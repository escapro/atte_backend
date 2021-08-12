from crm.utils import getSubdomain
from crm.permissions import isAdminManager, isClientUser, isEmployee, isManager
from main.serializers import ClientSerializer
from main.models import Client
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes


class ClientView(APIView):

    # permission_classes = (isClientUser, permissions.IsAuthenticated,)

    def get(self, request):

        subdomain = getSubdomain(request)

        queryset = Client.objects.get(name=subdomain)
        serializer_class = ClientSerializer(queryset)
        # permission_class = permissions.IsAuthenticated

        return Response(serializer_class.data)