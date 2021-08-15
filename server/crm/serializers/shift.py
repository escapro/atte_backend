from main.serializers.employee import EmployeeSerializer
from crm.serializers.shift_type import ShiftTypeSerializer
from rest_framework import serializers
from crm.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    shift_type = ShiftTypeSerializer()
    employee = EmployeeSerializer()

    class Meta:
        model = Shift
        fields = '__all__'

class ShiftCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shift
        fields = '__all__'