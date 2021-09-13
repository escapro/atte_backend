from crm.serializers.bonuses import BonuseCreateSerializer, BonuseSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser
from crm.models import Bonuses


class BonuseView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        bonuses = Bonuses.objects.order_by('revenue_to')
        serializer_class = BonuseSerializer(bonuses, many=True)

        return Response(serializer_class.data)


class CreateBonuseView(APIView):

    permission_classes = (isClientUser, isAdminManager)

    def post(self, request, format=None):
        serializer = BonuseCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({"error_fields":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)