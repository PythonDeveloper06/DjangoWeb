import pytz
import datetime
from rest_framework.viewsets import ModelViewSet

from .models import DeviceModel
from .models import Keys
from .serializers import DeviceSerializer, KeysSerializer
from rest_framework.response import Response

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        for query in queryset:
            date_time = datetime.datetime.now()
            if query.used == 'T':
                if date_time.replace(tzinfo=pytz.UTC) > query.time_end:
                    Keys.objects.get(pk=query.id).delete()

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
