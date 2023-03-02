"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.views import generic
from .models import *

NUMBERS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')

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






class CustomForm(UserCreationForm):
    username = forms.CharField(min_length=5, max_length=150, 
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))
    email = forms.EmailField(label='email', 
                             widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'E - mail'})) 
    password1 = forms.CharField(label=_('Password'), 
                                widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'})) 
    password2 = forms.CharField(label=_('Confirm password'), 
                                widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

    def username_clean(self): 
        username = self.cleaned_data['username'].lower() 
        new = User.objects.filter(username=username) 
        if new.count(): 
            raise ValidationError("User Already Exist") 
        return username 
 
    def email_clean(self): 
        email = self.cleaned_data['email'].lower() 
        new = User.objects.filter(email=email) 
        if new.count(): 
            raise ValidationError("Email Already Exist") 
        return email 
 
    def clean_password2(self): 
        password1 = self.cleaned_data['password1'] 
        password2 = self.cleaned_data['password2'] 
 
        if password1 and password2 and password1 != password2: 
            raise ValidationError("Password don't match") 
        return password2 
 
    def save(self, commit = True): 
        user = User.objects.create_user( 
            self.cleaned_data['username'], 
            self.cleaned_data['email'], 
            self.cleaned_data['password1'] 
        ) 
        return user



class SignUpView(generic.CreateView):
    form_class = CustomForm
    success_url = reverse_lazy('login')
    template_name = 'app/signup.html'


class AddDeviceModel(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rand_number = int(''.join(random.sample(NUMBERS, 4)))
        while len(str(rand_number)) != 4:
            rand_number = int(''.join(random.sample(NUMBERS, 4)))
        self.fields['auth_key'].initial = rand_number



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



