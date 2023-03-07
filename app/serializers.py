from rest_framework.serializers import ModelSerializer
from .models import DeviceModel


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = "__all__"
