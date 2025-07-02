from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('applications/', views.ApplicationListView.as_view(), name='application-list'),
    path('applications/create/', views.ApplicationCreateView.as_view(), name='application-create'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/response/', views.ApplicationResponseView.as_view(), name='application-response'),
    path('applications/<int:pk>/withdraw/', views.withdraw_application, name='application-withdraw'),
] 