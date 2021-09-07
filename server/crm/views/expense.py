from crm.utils.shift import get_employee_active_shift
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
        active_wd = get_active_working_day(create=False)

        if not active_wd:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        active_shift = get_employee_active_shift(user=request.user)

        if not active_shift:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        expenses = Expense.objects.filter(working_day=active_wd, cashbox=active_shift.cashbox)
        serializer = ExpenseSerializer(expenses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # check_wd = check_create_working_day()

        # def new_expense(working_day):
        #     data = request.data

        #     data['working_day'] = working_day.id

        #     try:
        #         serializer = ExpenseCreateUpdateSerializer(data=data)

        #         if serializer.is_valid():
        #             serializer.save()

        #             return Response(serializer.data, status=status.HTTP_201_CREATED)

        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #     except BaseException as error:
        #         return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        # if check_wd['success']:
        #     return new_expense(check_wd['object'])
        # else:
        #     return Response({"error": check_wd['message']}, status=status.HTTP_400_BAD_REQUEST)

        active_wd = get_active_working_day(create=False)

        if not active_wd:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        active_shift = get_employee_active_shift(user=request.user)

        if not active_shift:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ser_data = {}

        ser_data['working_day'] = active_wd.id
        ser_data['cashbox'] = active_shift.cashbox.id
        ser_data['shift_type'] = active_shift.shift_type.id
        ser_data['expense_category'] = request.data['expense_category'] if "expense_category" in request.data else None
        ser_data['time'] = request.data['time'] if "time" in request.data else None
        ser_data['who'] = request.data['who'] if "who" in request.data else None
        ser_data['whom'] = request.data['whom'] if "whom" in request.data else None
        ser_data['sum'] = request.data['sum'] if "sum" in request.data else None
        ser_data['comment'] = request.data['comment'] if "comment" in request.data else None

        serializer = ExpenseCreateUpdateSerializer(data=ser_data)
        
        if not serializer.is_valid():
            return Response({"error_fields":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)