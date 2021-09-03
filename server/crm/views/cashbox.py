from crm.serializers.cashbox import CashboxSerializer
from crm.models import Cashbox
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser


class CashboxView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        cashboxes = Cashbox.objects.filter(is_active=True).order_by('index')
        serializer_class = CashboxSerializer(cashboxes, many=True)

        return Response(serializer_class.data)