"""
Definition of urls for DjangoWeb.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.forms import SignUpView


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('devices/', views.devices, name="devices"),
    path('your_device/<int:pk>/update_form/', 
         views.DeviceUpdateView.as_view
         (
            extra_context= 
            {
                 'title': 'Update your device',
                 'year' : datetime.now().year
            }
         ), 
         name="update_form"),
    path('your_device/<int:pk>/delete_form/', 
         views.DeviceDeleteView.as_view
         (
            extra_context= 
            {
                 'title': 'Delete your device',
                 'year' : datetime.now().year
            }
         ), 
         name="delete_form"),
    path('your_device/<int:pk>/', 
         views.DeviceDetailView.as_view
         (  
             extra_context= 
             {
                 'title': 'Your Device',
                 'year' : datetime.now().year
                 }
         ), 
         name='your_device'),
    path('signup/', 
         SignUpView.as_view
         (
             extra_context= 
             {
                 'title': 'Sign up',
                 'year' : datetime.now().year,
             }
         ), 
         name="signup")
]
