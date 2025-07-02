from django.db import models
from users.models import User


class Team(models.Model):
    """Model for team formation"""
    
    name = models.CharField(max_length=100, unique=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
    
    def __str__(self):
        return f"{self.name} (Leader: {self.leader.username})"
    
    @property
    def member_count(self):
        return self.members.filter(status='accepted').count()
    
    @property
    def is_full(self):
        return self.member_count >= 4
    
    def can_add_member(self):
        return not self.is_full


class TeamMember(models.Model):
    """Model for team membership with invitation system"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    invited_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        unique_together = ['team', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.team.name} ({self.status})" 