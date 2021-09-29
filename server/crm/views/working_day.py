from crm.utils.shift import get_active_shifts, get_employee_active_shift
from crm.utils.working_day import calculate_wd_income, get_active_working_day
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser
from rest_framework import status
from crm.utils.common import debug


class CloseWdView(APIView):
    permission_classes = (isClientUser,)

    def post(self, request):
        active_wd = get_active_working_day(create=False)
        active_shifts = get_active_shifts()

        if active_shifts:
            return Response({"error_message": "Сначала нужно закрыть активную смену"},
                            status=status.HTTP_400_BAD_REQUEST)

        wd_income = calculate_wd_income()

        debug('wd_income', wd_income)

        active_wd.finished = True
        active_wd.cash_income = wd_income['cash_income']
        active_wd.noncash_income = wd_income['noncash_income']
        active_wd.total_income = wd_income['total_income']
        active_wd.save()

        return Response({"success": True}, status=status.HTTP_200_OK)