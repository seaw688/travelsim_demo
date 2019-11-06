from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CallRequest(models.Model):
    token = models.CharField(max_length=200, db_index=True)



CALL_STATUSES = (
    ('OTHER','Other'),
    ('ACCEPTED','Accepted'),
    ('REJECTED','Rejected'),
    ('ERROR','Error'),
    ('STARTED','Started'),
    ('ENDED','Ended')
)

class VoipCall(models.Model):
    call_id = models.CharField(max_length=100,blank=True,null=True)

    caller_number = models.CharField(max_length=40,blank=True,null=True)
    extension_number = models.CharField(max_length=40,blank=True,null=True)

    error_description = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(choices=CALL_STATUSES,default=CALL_STATUSES[0][0],max_length=20)

    user = models.ForeignKey(UserModel,on_delete=models.SET_NULL,null=True,blank=True)
    doctor = models.ForeignKey(UserModel,on_delete=models.SET_NULL,related_name='doctor_set',null=True,blank=True)

    call_request_time = models.DateTimeField(blank=True,null=True)
    call_start_time = models.DateTimeField(blank=True,null=True)
    call_ended_time = models.DateTimeField(blank=True,null=True)


