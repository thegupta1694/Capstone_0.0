from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/me/', views.current_user, name='current_user'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('professors/', views.ProfessorListView.as_view(), name='professor-list'),
    path('professors/<int:pk>/', views.ProfessorDetailView.as_view(), name='professor-detail'),
] 