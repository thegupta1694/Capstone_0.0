from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('teams/', views.TeamListView.as_view(), name='team-list'),
    path('teams/create/', views.TeamCreateView.as_view(), name='team-create'),
    path('teams/my/', views.MyTeamView.as_view(), name='my-team'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('teams/invite/', views.TeamInviteView.as_view(), name='team-invite'),
    path('teams/response/<int:pk>/', views.TeamResponseView.as_view(), name='team-response'),
    path('teams/invitations/', views.my_invitations, name='my-invitations'),
    path('teams/leave/', views.leave_team, name='leave-team'),
    path('teams/members/<int:member_id>/remove/', views.remove_member, name='remove-member'),
] 