from crm.serializers.shift_type import ShiftTypeSerializer
from crm.serializers.expense_category import ExpenseCategroySerializer
from rest_framework import serializers
from crm.models import Expense, ExpenseCategory


class ExpenseSerializer(serializers.ModelSerializer):
    expense_category = ExpenseCategroySerializer()
    shift_type = ShiftTypeSerializer()

    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Expense
        fields = '__all__'