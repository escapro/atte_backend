from main.models import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['name', 'paid_until', 'on_trial', 'created_on']