from crm.serializers.additional_expense_category import AdditionalExpenseCategorySerializer
from rest_framework import serializers
from crm.models import AdditionalExpense


class AdditionalExpenseSerializer(serializers.ModelSerializer):
    additional_expense_category = AdditionalExpenseCategorySerializer()

    class Meta:
        model = AdditionalExpense
        fields = '__all__'


class AdditionalExpenseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalExpense
        fields = '__all__'
        extra_kwargs = {
            'date': {'required': True}
        }