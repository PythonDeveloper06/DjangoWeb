"""
Definition of urls for DjangoWeb.
"""

from datetime import datetime

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.forms import SignUpView
from app.api import DeviceViewSet, KeysViewSet
from app.views import ChangePasswordView

from rest_framework_extensions.routers import ExtendedSimpleRouter


router = ExtendedSimpleRouter()
router.register(r'devices', DeviceViewSet, basename='DeviceViewSet') \
      .register(r'keys', KeysViewSet, basename='KeysViewSet', parents_query_lookups=['device'])


urlpatterns = [
    path('', views.home, name='home'),

    path('seld/', views.home, name='seld'),

    path('about/', views.about, name='about'),

    path('login/', LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context={'title': 'Log in', 'year' : datetime.now().year}
         ), 
         name='log_in'),

    path('logout/', LogoutView.as_view(next_page='/'), name='log_out'),

    path('admin/', admin.site.urls),

    path('devices/', views.DevicesListView.as_view(extra_context= {'title': 'Your devices', 'year' : datetime.now().year}), name="devices"),

    path('your_device/<int:pk>/update_form/', views.DeviceUpdateView.as_view
         (
            extra_context= {'title': 'Update your device', 'year' : datetime.now().year}
         ), 
         name="update_form"),

    path('your_device/<int:pk>/delete_form/', views.DeviceDeleteView.as_view
         (
            extra_context= 
            {'title': 'Delete your device', 'year' : datetime.now().year}
         ), 
         name="delete_form"),

    path('your_device/<int:pk>/', 
         views.DeviceDetailView.as_view
         (  
             extra_context= {'title': 'Your Device', 'year' : datetime.now().year}
         ), 
         name='your_device'),

    path('signup/', 
         SignUpView.as_view
         (
             extra_context={'title': 'Sign up', 'year' : datetime.now().year}
         ), 
         name="signup"),

    path('api/v1.0/', include(router.urls)),

    path('profile/', views.profile, name='profile'),

    path('change_password/', ChangePasswordView.as_view(), name='change_password'),

    path('your_device/<int:pk>/keys/', views.KeysListView.as_view(), name='keys'),

    path('your_device/<int:device_id>/keys/<int:pk>/delete_key_form/', 
         views.KeyDeleteView.as_view
         (
            extra_context= 
            {'title': 'Delete your key', 'year' : datetime.now().year}
         ),
         name='delete_key_form'
    ),

    path('api/v1.0/auth/', include('djoser.urls')),

    re_path(r'^auth/', include('djoser.urls.authtoken')),


    # !----- HTMX data -----!
    path('change_status/<int:pk>/', views.change_status, name='change_status'),
    path('change_device_name/<int:pk>/', views.change_device_name, name='change_device_name'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns 
