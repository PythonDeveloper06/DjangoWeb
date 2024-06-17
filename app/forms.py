"""
Definition of forms.
"""
from django.contrib.auth.models import User
from django.utils import timezone

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *

from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

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
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
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


# !----- Registration View -----!
class MyAuthForm(UserCreationForm):
    username = forms.CharField(label="Username",
                               max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'
                                }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'
                                }))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'
                                }))


class SignUpView(CreateView):
    form_class = MyAuthForm
    success_url = reverse_lazy('log_in')
    template_name = 'app/signup.html'


# !----- Profile View -----!
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter old password'
                                }))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Enter new password'
                                }))
    new_password2 = forms.CharField(label="New password confirmation", widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Confirm new password'
                                }))


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'app/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')


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
        self.fields['time_end'].initial = timezone.make_aware(datetime.datetime.now(), timezone=timezone.utc)
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



