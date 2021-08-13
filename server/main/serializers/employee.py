from main.serializers.user import UserSerializer
from main.serializers.client import ClientSerializer
from main.models import Employee
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    client = ClientSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeSerializerOnlyUser(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user']