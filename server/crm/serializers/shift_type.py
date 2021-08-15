from rest_framework import serializers
from crm.models import ShiftType


class ShiftTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShiftType
        fields = '__all__'
