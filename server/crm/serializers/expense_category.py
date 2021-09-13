from rest_framework import serializers
from crm.models import ExpenseCategory


class ExpenseCategroySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpenseCategroyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseCategory
        fields = ['name', 'is_accounting_expense']
        extra_kwargs = {
            'name': {'required': True},
            'is_accounting_expense': {'required': True},
        }