from crm.models import AdditionalExpense
from crm.serializers.additional_expense import AdditionalExpenseCreateSerializer, AdditionalExpenseSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser
from crm.utils.common import debug


class AdditionalExpenseView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):
        additioanl_expenses = AdditionalExpense.objects.all()
        serializer_class = AdditionalExpenseSerializer(additioanl_expenses, many=True)

        return Response(serializer_class.data, status=status.HTTP_200_OK)


class CreateAdditionalExpenseView(APIView):

    permission_classes = (isClientUser, isAdminManager,)

    def post(self, request):
        data = request.data
        
        if data['additional_expense_category'] == None and data['name'] == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if data['calculation_formula'] == None and data['sum'] == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if data['additional_expense_category'] and data['name']:
            del data['name']

        if data['calculation_formula'] and data['sum']:
            del data['calculation_formula']

        serializer = AdditionalExpenseCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({"error_fields":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)