"""
Definition of forms.
"""
import random
from django.contrib.auth.models import User
from django.utils import timezone

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


NUMBERS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')

DT = timezone.make_aware(datetime.datetime.now(), timezone=timezone.get_current_timezone())

def new_code():
    """Generate code"""
    number = random.randint(4, 16)
    rand_number = int(''.join(random.choices(NUMBERS, k=number)))
    return rand_number


class AddKeysModel(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(DT)
        self.fields['key'].initial = new_code()


    key = forms.CharField(min_length=4, max_length=16, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Key'}))
    time = forms.DateTimeField(initial=DT, required=True, widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Time'}))

    class Meta:
        model = Keys
        fields = '__all__'

        widgets = {
            'used': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Used'
                })
            }



