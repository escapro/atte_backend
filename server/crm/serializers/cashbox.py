from rest_framework import serializers
from crm.models import Cashbox


class CashboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cashbox
        fields = '__all__'
