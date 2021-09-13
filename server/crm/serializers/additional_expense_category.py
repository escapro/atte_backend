from rest_framework import serializers
from crm.models import AdditionalExpenseCategory


class AdditionalExpenseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalExpenseCategory
        fields = '__all__'


# class AdditionalExpenseCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ExpenseCategory
#         fields = ['name', 'is_accounting_expense']
#         extra_kwargs = {
#             'name': {'required': True},
#             'is_accounting_expense': {'required': True},
#         }