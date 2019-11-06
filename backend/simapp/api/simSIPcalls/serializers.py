from rest_framework import serializers
from call.models import VoipCall
from django.contrib.auth import get_user_model
from account.models import Profile
from api.medical_history.serializer import MedicalHistorySerializer
from  simpayments.models import DoctorCallPack
UserModel = get_user_model()



class UserProfileSer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','passport_image','date_birth','age','photo','document_id','travel_image','airline_image','medical_image','address','phone')

class UserSer(serializers.ModelSerializer):
    profile = UserProfileSer()
    medical_history = MedicalHistorySerializer(many=True)
    class Meta:
        model = UserModel
        fields = ('id','first_name','last_name','profile','medical_history')

class DoctorCallHistorySerializer(serializers.ModelSerializer):
    user = UserSer()
    class Meta:
        model = VoipCall
        fields = ('id','user','call_ended_time')


class CallHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = VoipCall
        fields = ('id','user','doctor','error_description','call_id','extension_number','caller_number','status','call_ended_time','call_start_time','call_request_time')

        depth =2


class DoctorCallPackSer(serializers.ModelSerializer):

    class Meta:
        model = DoctorCallPack
        fields = ('id','price','call_count')