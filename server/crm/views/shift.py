from crm.serializers.shift import ShiftCreateUpdateSerializer
from crm.serializers.expense import ExpenseSerializer
from crm.models import Expense
from crm.utils.shift_accounting import shift_fact
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser
from rest_framework import status


class ShiftView(APIView):

    permission_classes = (isClientUser,)

    def post(self, request):
        try:
            data = request.data

            serializer = ShiftCreateUpdateSerializer(data=data)

            if serializer.is_valid():
                cash_income = data['cash_end'] - data['cash_start']
                shift_expenses = Expense.objects.filter(date=data['date'])

                s = ExpenseSerializer(shift_expenses, many=True)

                print(data['date'])

                return Response(s.data)

                # serializer.save()
                # return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except BaseException as error:
            return Response({"error": "Произошла ошибка"}, status=status.HTTP_400_BAD_REQUEST)
