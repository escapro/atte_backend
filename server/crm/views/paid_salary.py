from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from crm.models import PaidSalaries
from crm.permissions import isAdminManager, isClientUser
from crm.serializers.paid_salaries import PaidSalarySerializer, PaidSalaryCreateSerializer
from crm.utils.common import debug


class PaidSalaryView(APIView):
    permission_classes = (isClientUser, isAdminManager)

    def get(self, request):
        if not request.GET.get('date_month') or not request.GET.get('date_year'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        params = {
            "date_month": request.GET.get('date_month'),
            "date_year": request.GET.get('date_year')
        }

        paid_salaries = PaidSalaries.objects.filter(date__month=params['date_month'], date__year=params['date_year'])
        serializer = PaidSalarySerializer(paid_salaries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePaidSalaryView(APIView):
    permission_classes = (isClientUser, isAdminManager)

    def post(self, request, format=None):
        serializer = PaidSalaryCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error_fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)