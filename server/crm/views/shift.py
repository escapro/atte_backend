from main.models import Employee
from crm.serializers.shift import ShiftCreateUpdateSerializer
from crm.models import Shift, ShiftTraker
from crm.utils.shift import calculate_shift_trackers, get_exist_active_shift
from crm.utils.common import check_create_working_day
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser, isEmployee
from rest_framework import status
import datetime


class CheckShiftView(APIView):
    permission_classes = (isClientUser,)

    def get(self, request):
        return Response(get_exist_active_shift(request), status=status.HTTP_200_OK)


class OpenShiftView(APIView):
    permission_classes = (isClientUser, isEmployee)

    def post(self, request):
        result = {
            'success': False,
            'message': "Произошла ошибка"
        }

        if get_exist_active_shift(request)['exist']:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        def create_shift():
            new_data = {}
            new_data['working_day'] = last_working_day.id
            new_data['shift_type'] = request.data['shift_type'] if request.data['shift_type'] else None
            new_data['employee'] = Employee.objects.get(user=request.user).id

            serializer = ShiftCreateUpdateSerializer(data=new_data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            else:
                return False

        try:
            last_working_day = check_create_working_day(create=True)

            if last_working_day['success']:
                last_working_day = last_working_day['object']
            else:
                result['message'] = last_working_day['message']

            last_shift = Shift.objects.filter(working_day=last_working_day).last()

            new_shift = None
            new_shift_tracker = None

            if last_shift:
                if last_shift.finished:
                    new_shift = create_shift()
                    if new_shift:
                        result['success'] = True
                else:
                    result['message'] = 'Чтобы открыть новую смену, надо закрыть предыдущую'
            else:
                new_shift = create_shift()
                if new_shift:
                    result['success'] = True

            if result['success']:
                shift_trackers = ShiftTraker.objects.filter(shift=new_shift['id'])

                if not len(shift_trackers) == 0:
                    result['success'] = False
                else:
                    today = datetime.datetime.fromisoformat(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
                    new_shift_tracker = ShiftTraker.objects.create(shift=Shift.objects.get(pk=new_shift['id']), action=ShiftTraker.START, datetime=today)
                    if new_shift_tracker:
                        result['message'] = ''
        except BaseException as error:
           print(error)

        return Response(result, status=status.HTTP_201_CREATED)

class ActiveShiftView(APIView):
    permission_classes = (isClientUser,)

    def get(self, request):
        result = {
            'success': False,
            'message': "",
            'data': None
        }

        last_working_day = check_create_working_day(create=False)

        if last_working_day['success']:
            last_working_day = last_working_day['object']
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        last_shift = Shift.objects.filter(working_day=last_working_day).last()

        if not last_shift:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        if not last_shift.employee.user == request.user:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        if last_shift.finished:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        shift_trackers = ShiftTraker.objects.filter(shift=last_shift).order_by('datetime').values()

        if not len(shift_trackers) >= 1:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        tracker_current_time = calculate_shift_trackers(shift_trackers)

        return Response(tracker_current_time, status=status.HTTP_200_OK)
    
    def put(self, request):
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

        if not last_shift.employee.user == request.user:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        if last_shift.finished:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        last_shift_tracker = ShiftTraker.objects.filter(shift=last_shift).order_by('datetime').last()

        if not last_shift_tracker:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        last_action = int(last_shift_tracker.action)
        current_action = request.data['action']

        if current_action == 1 or current_action == 4:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        if last_action == 1:
            if current_action == 1 or current_action == 3:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        elif last_action == 2:
            if current_action == 1 or current_action == 2:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        elif last_action == 3:
            if current_action == 1 or current_action == 3:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.datetime.fromisoformat(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

        if last_shift_tracker.datetime >= today:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        new_shift_tracker = ShiftTraker.objects.create(shift=last_shift, action=current_action, datetime=today)

        if not new_shift_tracker:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        shift_trackers = ShiftTraker.objects.filter(shift=last_shift).order_by('datetime').values()

        if not len(shift_trackers) >= 1:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        tracker_current_time = calculate_shift_trackers(shift_trackers)

        return Response(tracker_current_time, status=status.HTTP_200_OK)

class CloseShiftView(APIView):
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

        if not last_shift.employee.user == request.user:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        if last_shift.finished:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        shift_trackers = ShiftTraker.objects.filter(shift=last_shift).order_by('datetime')

        if len(shift_trackers) < 1:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.datetime.fromisoformat(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

        last_shift.finished = True
        last_shift.save()

        new_shift_tracker = ShiftTraker.objects.create(shift=last_shift, action=ShiftTraker.STOP, datetime=today)

        result['success'] = True

        return Response(result, status=status.HTTP_200_OK)

# class ShiftView(APIView):

#     permission_classes = (isClientUser,)

#     def post(self, request):
#         check_wd = check_working_day()

#         def is_valid_shift_type(shift_type_id, working_day):
#             result = True

#             shift_objects = Shift.objects.filter(working_day=working_day)
#             current_shift_type = ShiftType.objects.get(id=shift_type_id)

#             if shift_objects.filter(shift_type__id=shift_type_id).exists():
#                 result = False

#             for shift in shift_objects:
#                 if shift.shift_type.index >= current_shift_type.index:
#                     result = False

#             return result

#         def new_shift(working_day):
#             data = request.data

#             data['working_day'] = working_day.id

#             try:
#                 if not is_valid_shift_type(data['shift_type'], working_day):
#                        return Response({"error": "Произошла ошибка"}, status=status.HTTP_400_BAD_REQUEST)

#                 new_data = process_shift_data(data)

#                 serializer = ShiftCreateUpdateSerializer(data=new_data)
#                 if serializer.is_valid():
#                     result = {
#                         "success": False,
#                         "data": {
#                             "fact": serializer.validated_data['fact'],
#                             "cash_difference": serializer.validated_data['cash_difference'],
#                             "noncash_difference": serializer.validated_data['noncash_difference']
#                         }
#                     }

#                     if serializer.validated_data['fact']:
#                         serializer.validated_data['difference_report'] = ''
#                         result['success'] = True
#                     else:
#                         if serializer.validated_data['difference_report']:
#                             if serializer.validated_data['difference_report'].strip() != '':
#                                 result['success'] = True

#                     if result['success']:
#                         serializer.save()
#                         check_working_day_for_completness(working_day)

#                     return Response(result, status=status.HTTP_200_OK)

#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#             except BaseException as error:
#                 return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

#         if check_wd['success']:
#             return new_shift(check_wd['object'])
#         else:
#             return Response({"error": check_wd['message']}, status=status.HTTP_400_BAD_REQUEST)
