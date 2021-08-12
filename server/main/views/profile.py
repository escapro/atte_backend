from crm.utils import getUserClientInfo
from main.models import Admin, Employee, Manager
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from main.serializers import AdminSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics


# class ProfileView(generics.ListAPIView):
#     print(User._meta.pk.name)
#     serializer_class = UserSerializer
#     queryset = User.objects.all

class ProfileView(APIView):
    def get(self, request, format=None):

        data = {}
        data['username'] = request.user.username
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
        data['email'] = request.user.email

        user_client_info = getUserClientInfo(request.user)

        data['role'] = user_client_info['role']
        data['client'] = user_client_info['client']
        

        # employee = Employee.objects.filter(user=request.user)
        
        # if not employee:
        #     managers = Manager.objects.filter(user=request.user)
        #     if not managers:
        #         admin = Admin.objects.filter(user=request.user)
        #         if admin:
        #             data['role'] = 'admin'
        #     else:        
        #         if managers:
        #             data['role'] = 'manager'

        #             data['clients'] = []

        #             for manager in managers:
        #                 data['clients'].append(manager.client.name)
        # else:
        #     data['client'] = None
        #     employee = employee[0]
        #     data['client'] = employee.client.name
        #     data['role'] = 'employee'

        return Response(data)

        # if user.is_authenticated:
        #     return Admin.objects.filter(user=user)