from rest_framework import serializers
from .models import Application
from teams.serializers import TeamSerializer
from users.serializers import ProfessorProfileSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for applications"""
    
    team = TeamSerializer(read_only=True)
    professor = ProfessorProfileSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = ('id', 'team', 'professor', 'status', 'submitted_at', 'responded_at', 'message', 'professor_response')


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications"""
    
    class Meta:
        model = Application
        fields = ('professor', 'message')
    
    def validate(self, attrs):
        user = self.context['request'].user
        
        # Check if user is a student and has a team
        if user.role != 'student':
            raise serializers.ValidationError("Only students can submit applications")
        
        # Get user's team
        try:
            team = user.team_memberships.get(status='accepted').team
        except:
            raise serializers.ValidationError("You must be in a team to submit applications")
        
        # Check if team already has 4 pending applications
        pending_count = Application.objects.filter(team=team, status='pending').count()
        if pending_count >= 4:
            raise serializers.ValidationError("Your team already has 4 pending applications")
        
        # Check if professor has available slots
        professor = attrs['professor']
        if not professor.can_accept_application():
            raise serializers.ValidationError("This professor has no available slots")
        
        # Check if team already applied to this professor
        if Application.objects.filter(team=team, professor=professor).exists():
            raise serializers.ValidationError("Your team already applied to this professor")
        
        attrs['team'] = team
        return attrs


class ApplicationResponseSerializer(serializers.ModelSerializer):
    """Serializer for professor responses to applications"""
    
    class Meta:
        model = Application
        fields = ('status', 'professor_response')
    
    def validate_status(self, value):
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError("Status must be 'accepted' or 'rejected'")
        return value
    
    def validate(self, attrs):
        # Check if professor has available slots when accepting
        if attrs['status'] == 'accepted':
            professor = self.instance.professor
            if not professor.can_accept_application():
                raise serializers.ValidationError("No available slots to accept this application")
        
        return attrs 