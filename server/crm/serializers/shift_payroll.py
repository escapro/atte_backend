from rest_framework import serializers
from crm.models import ShiftPayroll
from crm.serializers.shift_payroll_period import ShiftPayrollPeriodSerializer


class ShiftPayrollSerializer(serializers.ModelSerializer):
    period = ShiftPayrollPeriodSerializer()

    class Meta:
        model = ShiftPayroll
        fields = '__all__'
