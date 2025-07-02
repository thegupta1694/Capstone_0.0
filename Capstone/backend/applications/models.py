from django.db import models
from users.models import ProfessorProfile
from teams.models import Team


class Application(models.Model):
    """Model for project applications from teams to professors"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='applications')
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    message = models.TextField(blank=True, null=True, help_text="Optional message from team to professor")
    professor_response = models.TextField(blank=True, null=True, help_text="Professor's response message")
    
    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        unique_together = ['team', 'professor']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.team.name} -> Prof. {self.professor.user.get_full_name()} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Update responded_at when status changes from pending
        if self.pk:
            old_instance = Application.objects.get(pk=self.pk)
            if old_instance.status == 'pending' and self.status != 'pending':
                from django.utils import timezone
                self.responded_at = timezone.now()
        
        super().save(*args, **kwargs)
        
        # If application is accepted, withdraw other pending applications from this team
        if self.status == 'accepted':
            Application.objects.filter(
                team=self.team,
                status='pending'
            ).exclude(pk=self.pk).update(status='withdrawn')
            
            # Increment professor's filled slots
            self.professor.filled_slots += 1
            self.professor.save() 