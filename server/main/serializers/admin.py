from main.models import Admin
from main.serializers.user import UserSerializer
from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = '__all__'
        error_messages = {"username": {"required": "Give yourself a username"}}