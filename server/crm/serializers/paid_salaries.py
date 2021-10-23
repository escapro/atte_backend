from rest_framework import serializers
from crm.models import PaidSalaries
from main.serializers.employee import EmployeeSerializer


class PaidSalarySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = PaidSalaries
        fields = '__all__'


class PaidSalaryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaidSalaries
        fields = ('employee', 'sum', 'date', 'comment')
        extra_kwargs = {
            'employee': {'required': True},
            'sum': {'required': True},
            'date': {'required': True},
        }