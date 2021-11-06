from main.serializers.user import UserCreateSerializer
from main.serializers.employee import EmployeeCreateSerializer, EmployeeSerializer, EmployeeSerializerOnlyUser
from main.models import Employee
from atte.constans import EMPLOYEE
from crm.utils.common import debug, getSubdomain, getUserClientInfo
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser
from rest_framework import status
from django.contrib.auth.models import User


class EmployeeView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        subdomain = getSubdomain(request)
        user_client_info = getUserClientInfo(request.user)

        employee = ''
        serializer_class = ''

        if(user_client_info['role'] == EMPLOYEE):
            employee = Employee.objects.filter(client__name=subdomain)
            serializer_class = EmployeeSerializerOnlyUser(employee, many=True)
        else:
            employee = Employee.objects.filter(client__name=subdomain)
            serializer_class = EmployeeSerializer(employee, many=True)

        return Response(serializer_class.data)


class CreateEmployeeView(APIView):

    permission_classes = (isClientUser, isAdminManager)

    def post(self, request, format=None):
        # new_user_serializer = UserCreateSerializer(data=request.data)
        #
        # if not new_user_serializer.is_valid():
        #     return Response({"error_fields": new_user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        #
        # new_user_serializer.save()
        #
        # created_user = User.objects.get(id=new_user_serializer.data['id'])

        created_user = User.objects.create_user(
            username=request.data['username'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            password=request.data['password'],
        )

        new_employee_data = {}
        new_employee_data['user'] = created_user.id
        new_employee_data['client'] = request.tenant.id

        new_employee_serializer = EmployeeCreateSerializer(data=new_employee_data)

        if not new_employee_serializer.is_valid():
            return Response({"error_fields": new_employee_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        new_employee_serializer.save()

        return Response(new_employee_serializer.data, status=status.HTTP_200_OK)
