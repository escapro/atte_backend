from main.models import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['name', 'paid_until', 'on_trial', 'created_on', 'permissible_cash_difference_plus', 'permissible_cash_difference_minus']


class ClientUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('shift_start_time', 'permissible_cash_difference_plus', 'permissible_cash_difference_minus')