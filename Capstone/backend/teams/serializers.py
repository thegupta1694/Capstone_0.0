from rest_framework import serializers
from users.models import User
from .models import Team, TeamMember


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for team members"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'department')


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for team members"""
    
    user = UserBasicSerializer(read_only=True)
    is_leader = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamMember
        fields = ('id', 'user', 'status', 'invited_at', 'responded_at', 'is_leader')
    
    def get_is_leader(self, obj):
        return obj.team.leader == obj.user


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for teams"""
    
    leader = UserBasicSerializer(read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    member_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    can_invite = serializers.SerializerMethodField()
    can_leave = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'leader', 'members', 'member_count', 'is_full', 'can_invite', 'can_leave', 'created_at', 'updated_at')
    
    def get_can_invite(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.leader == request.user and not obj.is_full
    
    def get_can_leave(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.leader != request.user


class TeamCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating teams"""
    
    class Meta:
        model = Team
        fields = ('name',)
    
    def validate_name(self, value):
        # Check if team name already exists
        if Team.objects.filter(name=value).exists():
            raise serializers.ValidationError("A team with this name already exists")
        return value
    
    def create(self, validated_data):
        validated_data['leader'] = self.context['request'].user
        return super().create(validated_data)


class TeamInviteSerializer(serializers.Serializer):
    """Serializer for team invitations"""
    
    user_id = serializers.IntegerField()
    
    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
            if user.role != 'student':
                raise serializers.ValidationError("Can only invite students to teams")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
    
    def create(self, validated_data):
        team = self.context['team']
        user = User.objects.get(id=validated_data['user_id'])
        
        # Check if team is full
        if not team.can_add_member():
            raise serializers.ValidationError("Team is already full")
        
        # Check if user is already in a team
        if TeamMember.objects.filter(user=user, status='accepted').exists():
            raise serializers.ValidationError("User is already in a team")
        
        # Check if user already has a pending invitation from this team
        existing_invitation = TeamMember.objects.filter(
            team=team,
            user=user,
            status='pending'
        ).first()
        
        if existing_invitation:
            raise serializers.ValidationError("User already has a pending invitation from this team")
        
        # Create team membership
        team_member = TeamMember.objects.create(
            team=team,
            user=user,
            status='pending'
        )
        
        return team_member


class TeamResponseSerializer(serializers.ModelSerializer):
    """Serializer for responding to team invitations"""
    
    class Meta:
        model = TeamMember
        fields = ('status',)
    
    def validate_status(self, value):
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError("Status must be 'accepted' or 'rejected'")
        return value
    
    def update(self, instance, validated_data):
        from django.utils import timezone
        
        instance.status = validated_data['status']
        instance.responded_at = timezone.now()
        instance.save()
        
        return instance


class TeamMemberDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for team member management"""
    
    user = UserBasicSerializer(read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    leader_name = serializers.CharField(source='team.leader.get_full_name', read_only=True)
    
    class Meta:
        model = TeamMember
        fields = ('id', 'user', 'team_name', 'leader_name', 'status', 'invited_at', 'responded_at') 