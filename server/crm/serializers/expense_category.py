from rest_framework import serializers
from crm.models import ExpenseCategory


class ExpenseCategroySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseCategory
        fields = '__all__'

class ExpenseCategroySerializerq(serializers.ModelSerializer):

    class Meta:
        model = ExpenseCategory
        fields = '__all__'