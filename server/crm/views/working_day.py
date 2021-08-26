from crm.models import Shift, ShiftTraker
from crm.utils.common import check_create_working_day
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser
from rest_framework import status
import datetime


class CloseWdView(APIView):
    permission_classes = (isClientUser,)

    def post(self, request):
        result = {
            'success': False,
            'message': "",
            'data': None
        }

        last_working_day = check_create_working_day(create=False)

        if not last_working_day['success']:
            result['message'] = last_working_day['message']
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        last_working_day = last_working_day['object']

        last_shift = Shift.objects.filter(working_day=last_working_day).last()

        if not last_shift:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        if not last_shift.finished:
            result['message'] = "Закройте пожалуйста смену"
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        last_working_day.finished = True
        last_working_day.save()

        result['success'] = True

        return Response({"success": True}, status=status.HTTP_200_OK)