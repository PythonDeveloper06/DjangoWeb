from rest_framework.viewsets import ModelViewSet

from .models import DeviceModel
from .models import Keys
from .serializers import DeviceSerializer, KeysSerializer

from rest_framework_extensions.mixins import NestedViewSetMixin


class DeviceViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = DeviceSerializer
    lookup_field = 'serial_num'

    def get_queryset(self):
        user = self.request.user
        return DeviceModel.objects.filter(user=user)


class KeysViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = KeysSerializer

    def get_queryset(self):
        s_num = self.kwargs['parent_lookup_device']
        device_lock = DeviceModel.objects.get(serial_num=s_num)
        keys = Keys.objects.filter(device_id=device_lock.id)
        return keys
