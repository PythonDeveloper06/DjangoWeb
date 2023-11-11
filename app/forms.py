"""
Definition of forms.
"""
from email.policy import default
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


# !!! Login Users !!!
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


# !!! Create Registration View !!!
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app/signup.html'


# !!! My form !!!
class AddDeviceModel(forms.ModelForm):
    serial_num = forms.CharField(min_length=12, max_length=12, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial number'}))

    class Meta:
        model = DeviceModel
        fields = '__all__'

        widgets = {
            'device_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Device name'
                }),
            'status': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Status'
                }),
            }

USED_CHOICES = (
    ('C', 'Constant'), 
    ('T', 'Temporary'), 
    ('O', 'One use')
)

class AddKeysModel(forms.ModelForm):
    key = forms.CharField(min_length=4, max_length=16, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Key'}))


    class Meta:
        model = Keys
        fields = '__all__'

        widgets = {
            'used': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Used'
                }),
            'time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Time'
                }),
            }



