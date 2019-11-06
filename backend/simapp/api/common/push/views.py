from rest_framework import generics
from simalerts.models import Alert, AlertFilterWord
from rest_framework.response import Response
from rest_framework import status
from api.views import custom_api_response
from api.utils import ERROR_API
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.common.push.serializers import PushDeviceSerializer
from common.models import PushDevice

class PushDeviceListCreate(generics.ListCreateAPIView):
    serializer_class = PushDeviceSerializer

    def get_queryset(self):
        if self.request.user.role == 'CUSTOMER':
            qs = PushDevice.objects.filter(user=self.request.user)
        elif self.request.user.role == 'ADMIN':
            qs = PushDevice.objects.all()
        else:
            qs= None
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if qs:
            ser =self.get_serializer_class()
            ser = ser(qs,many=True)
            return Response(custom_api_response(ser),status=status.HTTP_200_OK)
        else:
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


    def create(self, request, *args, **kwargs):
        ser = self.get_serializer_class()
        ser = ser(data=self.request.data,context={'request':self.request})
        if ser.is_valid():
            instance = ser.save()
            return Response(custom_api_response(ser),status=status.HTTP_200_OK)
        else:
            error = {"detail": ERROR_API['400'][1]}
            error_codes = [ERROR_API['400'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

