from rest_framework.serializers import *
from .models import DeviceModel


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = "__all__"
