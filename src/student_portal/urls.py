from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('events/', views.event_feed, name='event_feed'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('my-events/', views.my_registrations, name='my_registrations'),
    path('login/', views.custom_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]