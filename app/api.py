from .models import DeviceModel
from .models import Keys

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer
    lookup_field = 'serial_num'

    def get_queryset(self):
        user = self.request.user
        return DeviceModel.objects.filter(user=user)

    @action(methods=['get'], detail=True)
    def keys(self, request, serial_num=None):
        keys = Keys.objects.all()
        return Response({'keys': keys.values()})

