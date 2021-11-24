import datetime
from crm.serializers.daily_shift_schedule import DailyShiftScheduleCreateSerializer, DailyShiftScheduleSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser
from crm.models import DailyShiftSchedule


class DailyShiftScheduleView(APIView):
    permission_classes = (isClientUser,)

    def get(self, request):
        current_week = []
        last_week = []
        next_week = []

        cw = datetime.datetime.today()
        lw = datetime.datetime.today() - datetime.timedelta(days=7)
        nw = datetime.datetime.today() + datetime.timedelta(days=7)

        current_week_days = [cw + datetime.timedelta(days=i) for i in
                             range(0 - cw.weekday(), 7 - cw.weekday())]
        last_week_days = [lw + datetime.timedelta(days=i) for i in
                          range(0 - lw.weekday(), 7 - lw.weekday())]
        next_week_days = [nw + datetime.timedelta(days=i) for i in
                          range(0 - nw.weekday(), 7 - nw.weekday())]

        DayL = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'пятница', 'Суббота', 'Воскресенье']

        for week in current_week_days:
            daily_shift_schedule = DailyShiftSchedule.objects.filter(date=week.strftime('%Y-%m-%d'))
            current_week.append({
                "employee": None if not daily_shift_schedule else daily_shift_schedule[0].employee.user.first_name,
                "shift_type": None if not daily_shift_schedule else daily_shift_schedule[0].shift_type.id,
                "date": week.strftime('%Y.%m.%d'),
                "week": DayL[week.weekday()],
                "exist": False if not daily_shift_schedule else True,
            })


        for week in last_week_days:
            daily_shift_schedule = DailyShiftSchedule.objects.filter(date=week.strftime('%Y-%m-%d'))
            last_week.append({
                "employee": None if not daily_shift_schedule else True,
                "shift_type": None if not daily_shift_schedule else True,
                "date": week.strftime('%Y.%m.%d'),
                "week": DayL[week.weekday()],
                "exist": False if not daily_shift_schedule else True,
            })


        for week in next_week_days:
            daily_shift_schedule = DailyShiftSchedule.objects.filter(date=week.strftime('%Y-%m-%d'))
            next_week.append({
                "employee": None if not daily_shift_schedule else True,
                "shift_type": None if not daily_shift_schedule else True,
                "date": week.strftime('%Y.%m.%d'),
                "week": DayL[week.weekday()],
                "exist": False if not daily_shift_schedule else True,
            })

        return Response({
            "current_week": current_week,
            "last_week": last_week,
            "next_week": next_week
        }, status=status.HTTP_200_OK)


class CreateDailyShiftScheduleView(APIView):
    permission_classes = (isClientUser, isAdminManager)

    def post(self, request, format=None):
        serializer = DailyShiftScheduleCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error_fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
