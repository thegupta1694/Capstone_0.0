from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Application
from .serializers import (
    ApplicationSerializer, 
    ApplicationCreateSerializer, 
    ApplicationResponseSerializer
)


class ApplicationCreateView(generics.CreateAPIView):
    """API view for creating applications"""
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class ApplicationListView(generics.ListAPIView):
    """API view for listing applications"""
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'professor__user__department']
    search_fields = ['team__name', 'professor__user__first_name', 'professor__user__last_name']
    ordering_fields = ['submitted_at', 'responded_at']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'student':
            # Students can see their team's applications
            try:
                team = user.team_memberships.get(status='accepted').team
                return Application.objects.filter(team=team)
            except:
                return Application.objects.none()
        
        elif user.role == 'teacher':
            # Teachers can see applications to them
            try:
                professor_profile = user.professorprofile
                return Application.objects.filter(professor=professor_profile)
            except:
                return Application.objects.none()
        
        else:
            # Admins can see all applications
            return Application.objects.all()


class ApplicationDetailView(generics.RetrieveAPIView):
    """API view for application details"""
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'student':
            # Students can see their team's applications
            try:
                team = user.team_memberships.get(status='accepted').team
                return Application.objects.filter(team=team)
            except:
                return Application.objects.none()
        
        elif user.role == 'teacher':
            # Teachers can see applications to them
            try:
                professor_profile = user.professorprofile
                return Application.objects.filter(professor=professor_profile)
            except:
                return Application.objects.none()
        
        else:
            # Admins can see all applications
            return Application.objects.all()


class ApplicationResponseView(generics.UpdateAPIView):
    """API view for professor responses to applications"""
    serializer_class = ApplicationResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'teacher':
            # Teachers can respond to applications to them
            try:
                professor_profile = user.professorprofile
                return Application.objects.filter(professor=professor_profile, status='pending')
            except:
                return Application.objects.none()
        
        elif user.role == 'admin':
            # Admins can respond to any application
            return Application.objects.filter(status='pending')
        
        else:
            return Application.objects.none()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def withdraw_application(request, pk):
    """Withdraw a pending application"""
    try:
        application = Application.objects.get(pk=pk)
        
        # Check permissions
        user = request.user
        if user.role == 'student':
            # Students can withdraw their team's applications
            try:
                team = user.team_memberships.get(status='accepted').team
                if application.team != team:
                    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            except:
                return Response({'error': 'You must be in a team'}, status=status.HTTP_403_FORBIDDEN)
        
        elif user.role not in ['teacher', 'admin']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if application can be withdrawn
        if application.status != 'pending':
            return Response({'error': 'Can only withdraw pending applications'}, status=status.HTTP_400_BAD_REQUEST)
        
        application.status = 'withdrawn'
        application.save()
        
        return Response({'message': 'Application withdrawn successfully'})
        
    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND) 