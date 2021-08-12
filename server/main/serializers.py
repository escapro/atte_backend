from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['name', 'paid_until', 'on_trial', 'created_on']


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = '__all__'
        error_messages = {"username": {"required": "Give yourself a username"}}


class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    client = ClientSerializer()

    class Meta:
        model = Manager
        fields = '__all__'