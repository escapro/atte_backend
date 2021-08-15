from main.serializers.employee import EmployeeSerializer, EmployeeSerializerOnlyUser
from main.models import Employee
from atte.constans import EMPLOYEE
from crm.utils.common import getSubdomain, getUserClientInfo
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser


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
