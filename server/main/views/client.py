from crm.utils.common import debug, getSubdomain
from crm.permissions import isAdminManager, isClientUser
from main.serializers.client import ClientSerializer, ClientUpdateSerializer
from main.models import Client
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ClientView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        subdomain = getSubdomain(request)

        queryset = Client.objects.get(name=subdomain)
        serializer_class = ClientSerializer(queryset)

        return Response(serializer_class.data)


class UpdateClientView(APIView):

    permission_classes = (isClientUser, isAdminManager,)

    def put(self, request):

        # subdomain = getSubdomain(request)

        # queryset = Client.objects.get(name=subdomain)
        # serializer_class = ClientSerializer(queryset)

        # return Response(serializer_class.data)

        serializer = ClientUpdateSerializer(request.tenant, data=request.data)

        if not serializer.is_valid():
            return Response({"error_fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)