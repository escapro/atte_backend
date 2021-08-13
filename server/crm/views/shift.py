from crm.utils import getSubdomain, getUserClientInfo
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser
from crm.models import Shift
from crm.serializers.shift import ShiftSerializer
import time

class ShiftView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        shifts = Shift.objects.filter(is_active=True).order_by('shift_type')
        serializer_class = ShiftSerializer(shifts, many=True)

        return Response(serializer_class.data)