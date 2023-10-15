from .models import DeviceModel
from django.contrib.auth.models import User
from .models import Keys

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'serial_num'

    @action(methods=['get'], detail=True)
    def keys(self, request, serial_num=None):
        keys = Keys.objects.all()
        return Response({'keys': keys.values()})

