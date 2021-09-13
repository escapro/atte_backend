from rest_framework import serializers
from crm.models import ShiftType


class ShiftTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShiftType
        fields = '__all__'

class ShiftTypeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShiftType
        fields = ('name', 'index', 'hourly_rate', 'is_active')
        extra_kwargs = {
            'name': {'required': True},
            'index': {'required': True},
            'hourly_rate': {'required': True},
            'is_active': {'required': True},
        }

