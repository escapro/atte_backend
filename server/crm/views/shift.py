from crm.utils.shift_accounting import process_shift_data
from crm.utils.common import check_working_day, check_working_day_for_completness
from crm.serializers.shift import ShiftCreateUpdateSerializer
from crm.models import Expense, Shift, ShiftType
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser
from rest_framework import status


class ShiftView(APIView):

    permission_classes = (isClientUser,)

    def post(self, request):
        check_wd = check_working_day()

        def is_valid_shift_type(shift_type_id, working_day):
            result = True

            shift_objects = Shift.objects.filter(working_day=working_day)
            current_shift_type = ShiftType.objects.get(id=shift_type_id)

            if shift_objects.filter(shift_type__id=shift_type_id).exists():
                result = False

            for shift in shift_objects:
                if shift.shift_type.index >= current_shift_type.index:
                    result = False

            return result

        def new_shift(working_day):
            data = request.data

            data['working_day'] = working_day.id

            try:
                if not is_valid_shift_type(data['shift_type'], working_day):
                       return Response({"error": "Произошла ошибка"}, status=status.HTTP_400_BAD_REQUEST)
                  
                new_data = process_shift_data(data)
                
                serializer = ShiftCreateUpdateSerializer(data=new_data)
                if serializer.is_valid():
                    result = {
                        "success": False,
                        "data": {
                            "fact": serializer.validated_data['fact'],
                            "cash_difference": serializer.validated_data['cash_difference'],
                            "noncash_difference": serializer.validated_data['noncash_difference']
                        }
                    }

                    if serializer.validated_data['fact']:
                        serializer.validated_data['difference_report'] = ''
                        result['success'] = True
                    else:
                        if serializer.validated_data['difference_report']:
                            if serializer.validated_data['difference_report'].strip() != '':
                                result['success'] = True
                    
                    if result['success']:
                        serializer.save()
                        check_working_day_for_completness(working_day)

                    return Response(result, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except BaseException as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        if check_wd['success']:
            return new_shift(check_wd['object'])
        else:
            return Response({"error": check_wd['message']}, status=status.HTTP_400_BAD_REQUEST)