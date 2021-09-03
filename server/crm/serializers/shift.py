from django.db.models.expressions import F
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

class OpenShiftSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shift
        fields = '__all__'


class CloseShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ('cash_start',
                  'cash_end',
                  'noncash_start',
                  'noncash_end',
                  'sales',
                  'cashbox_fact',
                  'cash_refund',
                  'noncash_refund',
                  'finished',
                  'difference_report',
                  'cash_income',
                  'noncash_income',
                  'shift_income',
                  'cash_difference',
                  'noncash_difference',
                  'fact')
        extra_kwargs = {
            'cash_start': {'required': True},
            'cash_end': {'required': True}, 
            'noncash_start': {'required': True}, 
            'noncash_end': {'required': True}, 
            'sales': {'required': True}, 
            'cashbox_fact': {'required': True}, 
            'cash_refund': {'required': True}, 
            'noncash_refund': {'required': True},
            'finished': {'required': True},
            'difference_report': {'required': False},
            'cash_income': {'required': False},
            'noncash_income': {'required': False},
            'shift_income': {'required': False},
            'cash_difference': {'required': False},
            'noncash_difference': {'required': False},
            'fact': {'required': False}
        } 

    def update(self, instance, validated_data):
        instance.cash_start = validated_data.get('cash_start', instance.cash_start)
        instance.cash_end = validated_data.get('cash_end', instance.cash_end)
        instance.noncash_start = validated_data.get('noncash_start', instance.noncash_start)
        instance.noncash_end = validated_data.get('noncash_end', instance.noncash_end)
        instance.sales = validated_data.get('sales', instance.sales)
        instance.cashbox_fact = validated_data.get('cashbox_fact', instance.cashbox_fact)
        instance.cash_refund = validated_data.get('cash_refund', instance.cash_refund)
        instance.noncash_refund = validated_data.get('noncash_refund', instance.noncash_refund)
        instance.finished = validated_data.get('finished', instance.finished)
        instance.difference_report = validated_data.get('difference_report', instance.difference_report)
        instance.cash_income = validated_data.get('cash_income', instance.cash_income)
        instance.noncash_income = validated_data.get('noncash_income', instance.noncash_income)
        instance.shift_income = validated_data.get('shift_income', instance.shift_income)
        instance.cash_difference = validated_data.get('cash_difference', instance.cash_difference)
        instance.noncash_difference = validated_data.get('noncash_difference', instance.noncash_difference)
        instance.fact = validated_data.get('fact', instance.fact)
        instance.save()
        return instance
