from rest_framework.serializers import *
from .models import DeviceModel, Keys


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = "__all__"


class KeysSerializer(ModelSerializer):
    class Meta:
        model = Keys
        fields = "__all__"

