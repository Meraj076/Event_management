from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_participants, name='event_participants'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]