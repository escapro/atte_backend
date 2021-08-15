from main.serializers.client import ClientSerializer
from main.models import Admin
from main.serializers.user import UserSerializer
from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    client = ClientSerializer(many=True)

    class Meta:
        model = Admin
        fields = '__all__'