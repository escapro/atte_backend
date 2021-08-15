from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser
from crm.models import ShiftType
from crm.serializers.shift_type import ShiftTypeSerializer

class ShiftTypeView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        shift_types = ShiftType.objects.filter(is_active=True).order_by('index')
        serializer_class = ShiftTypeSerializer(shift_types, many=True)

        return Response(serializer_class.data)