from rest_framework import generics, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from .models import Team, TeamMember
from .serializers import (
    TeamSerializer, 
    TeamCreateSerializer, 
    TeamInviteSerializer, 
    TeamResponseSerializer,
    TeamMemberSerializer
)


class TeamCreateView(generics.CreateAPIView):
    """API view for creating teams"""
    serializer_class = TeamCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Check if user is already a team leader
        if Team.objects.filter(leader=self.request.user).exists():
            raise serializers.ValidationError("You are already a team leader")
        
        # Check if user is already in a team
        if TeamMember.objects.filter(user=self.request.user, status='accepted').exists():
            raise serializers.ValidationError("You are already in a team")
        
        team = serializer.save()
        
        # Automatically add the leader as the first team member
        TeamMember.objects.create(
            team=team,
            user=self.request.user,
            status='accepted',
            responded_at=timezone.now()
        )


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view for team details"""
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            # Students can only see their own team
            return Team.objects.filter(members__user=user, members__status='accepted')
        else:
            # Teachers and admins can see all teams
            return Team.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        team = self.get_object()
        user = request.user
        
        # Only team leader can delete the team
        if team.leader != user and user.role != 'admin':
            return Response(
                {'error': 'Only team leader or admin can delete the team'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)


class TeamInviteView(generics.CreateAPIView):
    """API view for inviting team members"""
    serializer_class = TeamInviteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['team'] = self.get_team()
        return context
    
    def get_team(self):
        team = get_object_or_404(Team, leader=self.request.user)
        return team


class TeamResponseView(generics.UpdateAPIView):
    """API view for responding to team invitations"""
    serializer_class = TeamResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TeamMember.objects.filter(user=self.request.user, status='pending')
    
    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            
            # If accepting, check if user is already in another team
            if request.data.get('status') == 'accepted':
                existing_team = TeamMember.objects.filter(
                    user=request.user, 
                    status='accepted'
                ).first()
                
                if existing_team:
                    return Response(
                        {'error': 'You are already in a team'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            return super().update(request, *args, **kwargs)


class MyTeamView(generics.RetrieveAPIView):
    """API view for getting current user's team"""
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        if user.role == 'student':
            # Get team where user is a member
            team_member = get_object_or_404(TeamMember, user=user, status='accepted')
            return team_member.team
        else:
            # Get team where user is leader
            return get_object_or_404(Team, leader=user)


class TeamListView(generics.ListAPIView):
    """API view for listing teams (admin/teacher only)"""
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'teacher']:
            return Team.objects.all().prefetch_related('members__user')
        else:
            return Team.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_invitations(request):
    """Get current user's pending team invitations"""
    invitations = TeamMember.objects.filter(
        user=request.user, 
        status='pending'
    ).select_related('team', 'team__leader')
    
    serializer = TeamMemberSerializer(invitations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def leave_team(request):
    """Allow a team member to leave their team"""
    user = request.user
    
    try:
        team_member = TeamMember.objects.get(user=user, status='accepted')
        team = team_member.team
        
        # Team leader cannot leave the team (they must delete it instead)
        if team.leader == user:
            return Response(
                {'error': 'Team leader cannot leave the team. Delete the team instead.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team_member.delete()
        return Response({'message': 'Successfully left the team'})
        
    except TeamMember.DoesNotExist:
        return Response(
            {'error': 'You are not in any team'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_member(request, member_id):
    """Remove a member from the team (team leader only)"""
    user = request.user
    
    try:
        team_member = TeamMember.objects.get(id=member_id)
        team = team_member.team
        
        # Check if user is the team leader
        if team.leader != user and user.role != 'admin':
            return Response(
                {'error': 'Only team leader can remove members'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cannot remove the team leader
        if team_member.user == team.leader:
            return Response(
                {'error': 'Cannot remove team leader'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team_member.delete()
        return Response({'message': 'Member removed successfully'})
        
    except TeamMember.DoesNotExist:
        return Response(
            {'error': 'Team member not found'}, 
            status=status.HTTP_404_NOT_FOUND
        ) 