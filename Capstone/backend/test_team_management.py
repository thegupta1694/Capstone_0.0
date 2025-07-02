#!/usr/bin/env python
"""
Test script for team management functionality.
This script creates sample users and teams for testing purposes.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_allocation.settings')
django.setup()

from users.models import User, ProfessorProfile
from teams.models import Team, TeamMember

def create_sample_data():
    """Create sample users and teams for testing"""
    
    print("Creating sample data for team management testing...")
    
    # Create sample students
    students_data = [
        {
            'username': '2021CS001',
            'email': 'student1@university.edu',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'student',
            'department': 'Computer Science'
        },
        {
            'username': '2021CS002',
            'email': 'student2@university.edu',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'student',
            'department': 'Computer Science'
        },
        {
            'username': '2021CS003',
            'email': 'student3@university.edu',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'role': 'student',
            'department': 'Computer Science'
        },
        {
            'username': '2021CS004',
            'email': 'student4@university.edu',
            'first_name': 'Alice',
            'last_name': 'Brown',
            'role': 'student',
            'department': 'Computer Science'
        },
        {
            'username': '2021CS005',
            'email': 'student5@university.edu',
            'first_name': 'Charlie',
            'last_name': 'Wilson',
            'role': 'student',
            'department': 'Computer Science'
        }
    ]
    
    # Create students
    students = []
    for student_data in students_data:
        user, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults=student_data
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created student: {user.username} - {user.get_full_name()}")
        students.append(user)
    
    # Create sample professors
    professors_data = [
        {
            'username': 'prof001',
            'email': 'prof1@university.edu',
            'first_name': 'Dr. Sarah',
            'last_name': 'Miller',
            'role': 'teacher',
            'department': 'Computer Science',
            'research_domains': 'AI, Machine Learning, Data Science',
            'total_slots': 3
        },
        {
            'username': 'prof002',
            'email': 'prof2@university.edu',
            'first_name': 'Dr. Michael',
            'last_name': 'Chen',
            'role': 'teacher',
            'department': 'Computer Science',
            'research_domains': 'Web Development, Software Engineering',
            'total_slots': 2
        }
    ]
    
    # Create professors
    professors = []
    for prof_data in professors_data:
        user, created = User.objects.get_or_create(
            username=prof_data['username'],
            defaults={k: v for k, v in prof_data.items() if k != 'research_domains' and k != 'total_slots'}
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created professor: {user.username} - {user.get_full_name()}")
        
        # Create professor profile
        profile, created = ProfessorProfile.objects.get_or_create(
            user=user,
            defaults={
                'research_domains': prof_data['research_domains'],
                'total_slots': prof_data['total_slots']
            }
        )
        if created:
            print(f"Created professor profile for: {user.get_full_name()}")
        
        professors.append(user)
    
    # Create sample teams
    teams_data = [
        {
            'name': 'Team Alpha',
            'leader': students[0],
            'members': [students[1], students[2]]
        },
        {
            'name': 'Team Beta',
            'leader': students[3],
            'members': [students[4]]
        }
    ]
    
    # Create teams
    for team_data in teams_data:
        team, created = Team.objects.get_or_create(
            name=team_data['name'],
            defaults={'leader': team_data['leader']}
        )
        if created:
            print(f"Created team: {team.name}")
            
            # Add leader as accepted member
            TeamMember.objects.get_or_create(
                team=team,
                user=team_data['leader'],
                defaults={'status': 'accepted'}
            )
            
            # Add other members as accepted
            for member in team_data['members']:
                TeamMember.objects.get_or_create(
                    team=team,
                    user=member,
                    defaults={'status': 'accepted'}
                )
                print(f"Added {member.get_full_name()} to {team.name}")
    
    # Create some pending invitations
    if len(students) >= 6:
        # Create a new team with pending invitations
        team_gamma, created = Team.objects.get_or_create(
            name='Team Gamma',
            defaults={'leader': students[0]}
        )
        
        if created:
            # Add leader as accepted member
            TeamMember.objects.get_or_create(
                team=team_gamma,
                user=students[0],
                defaults={'status': 'accepted'}
            )
            
            # Create pending invitations for remaining students
            for student in students[1:4]:
                TeamMember.objects.get_or_create(
                    team=team_gamma,
                    user=student,
                    defaults={'status': 'pending'}
                )
                print(f"Created pending invitation for {student.get_full_name()} to join {team_gamma.name}")
    
    print("\nSample data creation completed!")
    print("\nTest accounts created:")
    print("Students:")
    for student in students:
        print(f"  Username: {student.username}, Password: password123")
    print("\nProfessors:")
    for prof in professors:
        print(f"  Username: {prof.username}, Password: password123")
    
    print("\nYou can now test the team management functionality!")

if __name__ == '__main__':
    create_sample_data() 