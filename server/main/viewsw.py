from rest_framework.serializers import Serializer
from crm.serializers import AdminSerializer, ManagerSerializer
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

import json
from django.core.serializers.json import DjangoJSONEncoder

class Logout(APIView):
    def get(self, request, fromat=None):
        request.user.auth_token.delete()
        return Response(status="OK")


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def __init__(self):
#         super(self)
#         pass
    
#     def validate(self, attrs):
#         print(self.default_error_messages)
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)

#         data['token'] = {}
#         data['token']['refresh'] = str(refresh)
#         data['token']['access'] = str(refresh.access_token)

#         del data['refresh']
#         del data['access']

#         # Add extra responses here
#         data['username'] = self.user.username
#         data['role'] = None

#         employee = Employee.objects.filter(user=self.user)
        
#         if not employee:
#             managers = Manager.objects.filter(user=self.user)
#             if not managers:
#                 admin = Admin.objects.filter(user=self.user)
#                 if admin:
#                     data['role'] = 'admin'
#             else:        
#                 if managers:
#                     data['role'] = 'manager'

#                     data['projects'] = []

#                     for manager in managers:
#                         data['projects'].append(manager.client.name)
#         else:
#             data['project'] = None
#             employee = employee[0]
#             data['project'] = employee.client.name
#             data['role'] = 'employee'


            
#         if not data['role']:
#             raise AuthenticationFailed

#         return data


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer