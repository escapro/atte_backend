from crm.serializers import ShiftSerializer
from crm.models import Shift
from main.serializers import ClientSerializer
from main.models import Client
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ShiftView(APIView):
    def get(self, request):

        queryset = Shift.objects.all()
        serializer_class = ShiftSerializer(queryset)

        return Response({})