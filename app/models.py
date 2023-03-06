"""
Definition of models.
"""
from django.db import models
from django.urls import reverse_lazy
from django_userforeignkey.models.fields import UserForeignKey


class DeviceModel(models.Model):
    device_name = models.CharField(max_length=255)
    serial_num = models.CharField(max_length=255)
    auth_key = models.IntegerField(null=False)
    status = models.CharField(max_length=10, default="Close")
    user = UserForeignKey(auto_user_add=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse_lazy('devices')




