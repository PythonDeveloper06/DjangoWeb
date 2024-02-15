"""
Definition of forms.
"""
from django.contrib.auth.models import User
from django.utils import timezone

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *

import datetime
from .others import new_code


# !----- Profile form -----!
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


# !----- Login Users -----!
class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username",
                               max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'
                                }))
    password = forms.CharField(widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'
                                }))


# !---- Registration View -----!
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app/signup.html'


# !---- Device form -----!
class AddDeviceModel(forms.ModelForm):
    class Meta:
        model = DeviceModel
        fields = '__all__'

        widgets = {
            'device_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Device name',
                'name': 'device_name'
                }),
            'status': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Status'
                }),
            }


# !----- Key form -----!
class AddKeysModel(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_end'].initial = timezone.make_aware(datetime.datetime.now(), timezone=timezone.get_current_timezone())
        self.fields['key'].initial = new_code()


    key = forms.CharField(min_length=4, max_length=16, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Key'}))
    time_end = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Time'}))

    class Meta:
        model = Keys
        fields = '__all__'

        widgets = {
            'used': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Used'
                }),
            'selection': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Quick selection'
                })
            }



