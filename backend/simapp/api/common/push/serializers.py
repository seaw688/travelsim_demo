from rest_framework import serializers
from common.models import PushDevice


class PushDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PushDevice
        fields = ('pk','player_id','device_id')

    def save(self, **kwargs):
        instance = PushDevice.objects.create(user=self.context['request'].user,
                                             player_id=self.validated_data['player_id'],
                                             device_id=self.validated_data['device_id']
                                             )
        return instance
