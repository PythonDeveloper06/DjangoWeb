from .models import DeviceModel
from django.contrib.auth.models import User

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import DeviceSerializer


class DeviceViewSet(ReadOnlyModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceSerializer

    @action(methods=['get'], detail=True)
    def users(self, request, pk=None):
        every_user = User.objects.get(pk=pk)
        return Response({'users': every_user.username})
