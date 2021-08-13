from main.models import Manager
from main.serializers.client import ClientSerializer
from main.serializers.user import UserSerializer
from rest_framework import serializers


class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    client = ClientSerializer()

    class Meta:
        model = Manager
        fields = '__all__'