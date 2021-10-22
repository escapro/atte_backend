from rest_framework import serializers
from crm.models import Bonuses
from crm.serializers.shift_type import ShiftTypeSerializer


class BonuseSerializer(serializers.ModelSerializer):
    shift_type = ShiftTypeSerializer()

    class Meta:
        model = Bonuses
        fields = '__all__'


class BonuseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bonuses
        fields = ('shift_type', 'revenue_to', 'rate')
        extra_kwargs = {
            'shift_type': {'required': True},
            'revenue_to': {'required': True},
            'rate': {'required': True},
        }

