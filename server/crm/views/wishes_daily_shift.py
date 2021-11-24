from crm.serializers.daily_shift_schedule import DailyShiftScheduleCreateSerializer, DailyShiftScheduleSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser
from crm.models import WishesDailyShift


class WishesDailyShiftView(APIView):
    permission_classes = (isClientUser,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class CreateDailyShiftScheduleView(APIView):
    permission_classes = (isClientUser, isAdminManager)

    def post(self, request, format=None):
        serializer = DailyShiftScheduleCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error_fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
