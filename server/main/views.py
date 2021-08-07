from crm.serializers import AdminSerializer
from django.shortcuts import render
from rest_framework.response import Response

from .models import *
# from .serializers import *

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import AuthenticationFailed

class Logout(APIView):
    def get(self, request, fromat=None):
        request.user.auth_token.delete()
        return Response(status="OK")

class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
        

class AdminListView(generics.ListCreateAPIView):
    serializer_class = AdminSerializer
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Admin.objects.filter(user=user)
            
        raise PermissionDenied()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['role'] = None

        employee = Employee.objects.filter(user=self.user)
        
        if not employee:
            manager = Manager.objects.filter(user=self.user)
            if manager:
                data['role'] = 'manager'
        else:
             data['role'] = 'employee'
            
        if not data['role']:
            raise AuthenticationFailed

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer