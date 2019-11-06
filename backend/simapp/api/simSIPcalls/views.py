from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.views import custom_api_response
from django.contrib.auth import get_user_model
from call.models import VoipCall
from rest_framework import generics
from api.utils import ERROR_API
from api.views import CustomPagination, prepare_paginated_response

UserModel = get_user_model()

key = '3de914b014efc6bb80f18b6f08b24192fab5d129'
from call.models import VoipCall
from .serializers import DoctorCallHistorySerializer,CallHistorySerializer

class CallHistoryView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination


    def get_queryset(self):
        if self.request.user.role == 'DOCTOR':
            queryset = VoipCall.objects.filter(doctor=self.request.user).order_by('call_ended_time')
        if self.request.user.role == 'ADMIN':
            queryset = VoipCall.objects.all().order_by('call_ended_time')

        return queryset

    def get_serializer_class(self):
        ser_class=None
        if self.request.user.role == 'DOCTOR':
            ser_class = DoctorCallHistorySerializer
        if self.request.user.role == 'ADMIN':
            ser_class = CallHistorySerializer

        return ser_class




    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset.exists():
            paginate = prepare_paginated_response(self, request, queryset)
            if paginate:
                return Response(custom_api_response(content=paginate.content, metadata=paginate.metadata),
                            status=status.HTTP_200_OK)

            ser_class = self.get_serializer_class()

            ser = ser_class(queryset,many=True,context={"request":request})
        else:
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(custom_api_response(ser),status=status.HTTP_200_OK)




@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def CallInitiationCallback(request):
    if request.method == 'POST':
        return Response({'status': 'reject', 'error': 'Method POST not allowed'}, status=status.HTTP_400_BAD_REQUEST)

    token = request.GET.get('token', None)
    if token == None or token != key:
        return Response({'status': 'reject', 'error': 'Wrong token'}, status=status.HTTP_400_BAD_REQUEST)

    caller_number = request.GET.get('caller_number', None)
    if caller_number == '' or caller_number == None:
        return Response({'status': 'reject', 'error': 'Caller number not provided'}, status=status.HTTP_400_BAD_REQUEST)


    call_id = request.GET.get('call_id', None)
    if call_id == '' or call_id == None:
        return Response({'status': 'reject', 'error': 'Call id not provided'}, status=status.HTTP_400_BAD_REQUEST)

    voip_call, created = VoipCall.objects.get_or_create(call_id=call_id)

    try:
        user = UserModel.objects.get(profile__phone=caller_number)
    except UserModel.MultipleObjectsReturned:
        #voip_call = VoipCall(call_id=call_id, status='ERROR', error_description='User number duplication',
        #                     caller_number=caller_number, call_request_time=timezone.now())
        voip_call.status='ERROR'
        voip_call.error_description='User number duplication'
        voip_call.caller_number=caller_number
        voip_call.call_request_time=timezone.now()
        voip_call.save()
        return Response({'status': 'reject', 'error': 'Internal error.User duplication'},
                        status=status.HTTP_400_BAD_REQUEST)
    except UserModel.DoesNotExist:
        #voip_call = VoipCall(call_id=call_id, status='ERROR', error_description='User not found',
        #                     caller_number=caller_number, call_request_time=timezone.now())

        voip_call.status = 'ERROR'
        voip_call.error_description = 'User not found'
        voip_call.caller_number = caller_number
        voip_call.call_request_time = timezone.now()
        voip_call.save()
        return Response({'status': 'unregistered', 'error': 'Internal error.User not founded'},
                        status=status.HTTP_400_BAD_REQUEST)

    if user.profile.call_points >= 1:
        #voip_call = VoipCall(call_id=call_id, status='ACCEPTED', caller_number=caller_number, user=user,
        #                     call_request_time=timezone.now())
        voip_call.status = 'ACCEPTED'
        voip_call.user=user
        voip_call.caller_number = caller_number
        voip_call.call_request_time = timezone.now()
        voip_call.save()

        return Response({'status': 'accept'}, status=status.HTTP_200_OK)

    else:
        #voip_call = VoipCall(call_id=call_id, status='REJECTED', error_description='Bad user balance',
        #                     caller_number=caller_number, user=user, call_request_time=timezone.now())
        voip_call.status = 'REJECTED'
        voip_call.user = user
        voip_call.error_description ='Bad user balance'
        voip_call.caller_number = caller_number
        voip_call.call_request_time = timezone.now()
        voip_call.save()
        return Response({'status': 'reject'}, status=status.HTTP_200_OK)



@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def CallStartedCallback(request):
    if request.method == 'POST':
        return Response({'status': 'reject', 'error': 'Method POST not allowed'}, status=status.HTTP_400_BAD_REQUEST)

    token = request.GET.get('token', None)
    if token == None or token != key:
        return Response({'status': 'reject', 'error': 'Wrong token'}, status=status.HTTP_400_BAD_REQUEST)

    caller_number = request.GET.get('caller_number', None)

    if caller_number == '' or caller_number == None:
        return Response({'status': 'reject', 'error': 'Caller number not provided'}, status=status.HTTP_400_BAD_REQUEST)

    extension_number = request.GET.get('extension_number', None)

    if extension_number == '' or extension_number == None:
        return Response({'status': 'reject', 'error': 'Extension number not provided'},
                        status=status.HTTP_400_BAD_REQUEST)

    start_stamp = request.GET.get('start_stamp', None)

    if start_stamp == '' or start_stamp == None:
        return Response({'status': 'reject', 'error': 'Start time not provided or wrong format'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        time = datetime.strptime(start_stamp, '%Y-%m-%d-%H:%M')
    except ValueError:
        return Response({'status': 'reject', 'error': 'Start time not provided or wrong format'},
                        status=status.HTTP_400_BAD_REQUEST)

    call_id = request.GET.get('call_id', None)
    if call_id == '' or call_id == None:
        return Response({'status': 'reject', 'error': 'Call id not provided'}, status=status.HTTP_400_BAD_REQUEST)



    try:
        user = UserModel.objects.get(profile__phone=caller_number)
    except UserModel.MultipleObjectsReturned:
        user = None
    except UserModel.DoesNotExist:
        user = None

    try:
        doctor = UserModel.objects.get(profile__extension_number=extension_number)
    except UserModel.MultipleObjectsReturned:
        doctor = UserModel.objects.filter(profile__extension_number=extension_number).first()
    except UserModel.DoesNotExist:
        doctor = None



    try:
        voip_call=VoipCall.objects.get(call_id=call_id)

        voip_call.extension_number=extension_number
        voip_call.status='STARTED'
        voip_call.call_start_time=time
        voip_call.doctor=doctor

        voip_call.save()


    except VoipCall.DoesNotExist:
        voip_call = VoipCall(call_id=call_id,
                             extension_number=extension_number,
                             caller_number=caller_number,
                             status='STARTED',
                             call_start_time = time,
                             user = user,
                             doctor=doctor)
        voip_call.save()

    if user==None:
        voip_call.error_description = 'User not founded'
        voip_call.status = 'ERROR'
        voip_call.save()

    if doctor == None:
        voip_call.status = 'ERROR'
        if voip_call.error_description == None:
            voip_call.error_description = 'Doctor not founded'
        else:
            voip_call.error_description = voip_call.error_description + ' Doctor not founded'
        voip_call.save()


    return Response({'status': 'accept'}, status=status.HTTP_200_OK)





@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def CallEndedCallback(request):
    if request.method == 'POST':
        return Response({'status': 'reject', 'error': 'Method POST not allowed'}, status=status.HTTP_400_BAD_REQUEST)

    token = request.GET.get('token', None)
    if token == None or token != key:
        return Response({'status': 'reject', 'error': 'Wrong token'}, status=status.HTTP_400_BAD_REQUEST)

    caller_number = request.GET.get('caller_number', None)


    if caller_number == '' or caller_number == None:
        return Response({'status': 'reject', 'error': 'Caller number not provided'}, status=status.HTTP_400_BAD_REQUEST)

    extension_number = request.GET.get('extension_number', None)

    if extension_number == '' or extension_number == None:
        return Response({'status': 'reject', 'error': 'Extension number not provided'},
                        status=status.HTTP_400_BAD_REQUEST)

    end_stamp = request.GET.get('end_stamp', None)

    if end_stamp == '' or end_stamp == None:
        return Response({'status': 'reject', 'error': 'End time not provided or wrong format'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        time = datetime.strptime(end_stamp, '%Y-%m-%d-%H:%M')
    except ValueError:
        return Response({'status': 'reject', 'error': 'End time not provided or wrong format'},
                        status=status.HTTP_400_BAD_REQUEST)

    call_id = request.GET.get('call_id', None)
    if call_id == '' or call_id == None:
        return Response({'status': 'reject', 'error': 'Call id not provided'}, status=status.HTTP_400_BAD_REQUEST)


    try:
        user = UserModel.objects.get(profile__phone=caller_number)
        user.profile.call_points=user.profile.call_points-1
    except UserModel.MultipleObjectsReturned:
        user = None
    except UserModel.DoesNotExist:
        user = None


    try:
        doctor = UserModel.objects.get(profile__extension_number=extension_number)
    except UserModel.MultipleObjectsReturned:
        doctor = UserModel.objects.filter(profile__extension_number=extension_number).first()
    except UserModel.DoesNotExist:
        doctor = None



    try:
        voip_call=VoipCall.objects.get(call_id=call_id)

        voip_call.extension_number=extension_number
        voip_call.status='ENDED'
        voip_call.call_ended_time=time
        voip_call.doctor=doctor

        voip_call.save()


    except VoipCall.DoesNotExist:
        voip_call = VoipCall(call_id=call_id,
                             extension_number=extension_number,
                             caller_number=caller_number,
                             status='ENDED',
                             call_ended_time = time,
                             user = user,
                             doctor=doctor)
        voip_call.save()

    if not user==None:
        user.profile.save()
    else:
        voip_call.error_description='User not founded'
        voip_call.status = 'ERROR'
        voip_call.save()

    if doctor == None:
        voip_call.status = 'ERROR'
        if voip_call.error_description == None:
            voip_call.error_description = 'Doctor not founded'
        else:
            voip_call.error_description = voip_call.error_description + ' Doctor not founded'
        voip_call.save()


    return Response({'status': 'accept'}, status=status.HTTP_200_OK)



class CurrentCallUserInfo(generics.ListAPIView):



    def list(self, request, *args, **kwargs):
        if self.request.user.role != "DOCTOR":
            error = {"detail": ERROR_API['117'][1]}
            error_codes = [ERROR_API['117'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        current_call = VoipCall.objects.filter(doctor=self.request.user,status='STARTED').order_by('call_start_time').first()


        if current_call != None:

            ser_class = DoctorCallHistorySerializer

            ser = DoctorCallHistorySerializer(current_call,context={"request":request})

            return Response(custom_api_response(ser),status=status.HTTP_200_OK)

        else:
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)



from .serializers import DoctorCallPackSer
from simpayments.models import DoctorCallPack
class ListVoipCallsPack(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DoctorCallPackSer

    def get_queryset(self):
        qs = DoctorCallPack.objects.all()
        return qs



    def list(self, request, *args, **kwargs):
        ser = self.get_serializer_class()
        qs = self.get_queryset()
        if qs.exists():
            ser = ser(qs,many=True)
            return Response(custom_api_response(ser),status=status.HTTP_200_OK)
        else:
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view,authentication_classes, permission_classes

@api_view(('GET','POST'))
@permission_classes((AllowAny,))

def CallbackCheck(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})