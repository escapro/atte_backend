from rest_framework import serializers
from crm.models import Bonuses, DailyShiftSchedule


class DailyShiftScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyShiftSchedule
        fields = '__all__'


class DailyShiftScheduleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyShiftSchedule
        fields = ('employee', 'shift_type', 'date')
        extra_kwargs = {
            'employee': {'required': True},
            'shift_type': {'required': True},
            'date': {'required': True},
        }