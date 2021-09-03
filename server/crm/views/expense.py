from crm.utils.working_day import get_active_working_day
from crm.serializers.expense import ExpenseCreateUpdateSerializer, ExpenseSerializer
from crm.models import Expense, WorkingDay
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser
from rest_framework import status


class ExpenseView(APIView):
    permission_classes = (isClientUser, isAdminManager)

    def get(self, request):

        expenses = Expense.objects.all()
        serializer_class = ExpenseSerializer(expenses, many=True)

        return Response(serializer_class.data)


class ShiftExpensesView(APIView):
    permission_classes = (isClientUser,)

    def get(self, request):
        check_wd = get_active_working_day()

        expenses = Expense.objects.filter(working_day=check_wd['object'])
        serializer_class = ExpenseSerializer(expenses, many=True)

        return Response(serializer_class.data)

    def post(self, request):
        check_wd = check_create_working_day()

        def new_expense(working_day):
            data = request.data

            data['working_day'] = working_day.id

            try:
                serializer = ExpenseCreateUpdateSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except BaseException as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        if check_wd['success']:
            return new_expense(check_wd['object'])
        else:
            return Response({"error": check_wd['message']}, status=status.HTTP_400_BAD_REQUEST)