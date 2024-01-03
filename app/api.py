from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DeviceModel
from .models import Keys
from .serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer
    lookup_field = 'serial_num'

    def get_queryset(self):
        user = self.request.user
        return DeviceModel.objects.filter(user=user)

    @action(methods=['get'], detail=True)
    def keys(self, request, serial_num=None):
        device_lock = DeviceModel.objects.get(serial_num=serial_num)
        keys = Keys.objects.filter(device_id=device_lock.id)
        return Response({'keys': keys.values()})

