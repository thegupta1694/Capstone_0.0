from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    
    # Override username to use university ID
    username = models.CharField(
        max_length=50,
        unique=True,
        help_text="University ID (e.g., 2021CS001)"
    )
    
    # Add role field
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )
    
    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"


class ProfessorProfile(models.Model):
    """Extended profile for professors with research domains and slot management"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    research_domains = models.TextField(
        help_text="Comma-separated research domains (e.g., AI, ML, Web Development)"
    )
    bio = models.TextField(blank=True, null=True)
    total_slots = models.PositiveIntegerField(default=5)
    filled_slots = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Professor Profile'
        verbose_name_plural = 'Professor Profiles'
    
    def __str__(self):
        return f"Prof. {self.user.get_full_name()}"
    
    @property
    def available_slots(self):
        return self.total_slots - self.filled_slots
    
    def can_accept_application(self):
        return self.available_slots > 0 