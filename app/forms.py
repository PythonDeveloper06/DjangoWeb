"""
Definition of forms.
"""
import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *


NUMBERS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')


def new_code():
    rand_number = int(''.join(random.sample(NUMBERS, 4)))
    while len(str(rand_number)) != 4:
        rand_number = int(''.join(random.sample(NUMBERS, 4)))
    return rand_number


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


class CustomUserCreationForm(UserCreationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))
    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    password2 = forms.CharField(label=_("Confirm password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Confirm password'}))


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app/signup.html'


class AddDeviceModel(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['auth_key'].initial = new_code()
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['serial_num'].widget.attrs['readonly'] = True


    class Meta:
        model = DeviceModel
        fields = '__all__'

        widgets = {
            'device_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Device name'
                }),
            'serial_num': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Serial number'
                }),
            'auth_key': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'A random code will be generated here',
                'readonly': 'readonly',
                }),
            'status': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Status'
                }),
            }



