"""
Definition of models.
"""
from django.db import models
from django.urls import reverse_lazy
from django_userforeignkey.models.fields import UserForeignKey
from django.contrib.auth.models import User
from django.utils.timezone import now

from PIL import Image


class DeviceModel(models.Model):
    device_name = models.CharField(max_length=255)
    serial_num = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, default="Close")
    settings = models.CharField(max_length=255, default='-')
    admin = models.CharField(max_length=10, default='Off')
    sync = models.CharField(max_length=5, default='False')
    user = UserForeignKey(auto_user_add=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse_lazy('devices')

    def get_queryset(self):
        user = self.request.user
        queryset = self.model.objects.filter(user=user)
        return queryset


class Profile(models.Model):
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Keys(models.Model):
    USED_CHOICES = [
        ('C', 'Constant'),
        ('T', 'Temporary'),
        ('O', 'One use')
    ]

    SELECT_CHOICES = [
        ('-', '0'),
        ('+1h', '1 hour'),
        ('+1d', '1 day'),
        ('+1w', '1 week'),
        ('+2w', '2 week'),
    ]

    key = models.IntegerField()
    used = models.CharField(max_length=10, choices=USED_CHOICES, default='T')
    time_start = models.DateTimeField(null=True)
    time_end = models.DateTimeField(null=True)
    selection = models.CharField(max_length=100, choices=SELECT_CHOICES, default='-')
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)

    objects = models.Manager()
