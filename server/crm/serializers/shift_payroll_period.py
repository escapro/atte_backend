from rest_framework import serializers
from crm.models import ShiftPayrollPeriod


class ShiftPayrollPeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShiftPayrollPeriod
        fields = ('day', 'is_active')
