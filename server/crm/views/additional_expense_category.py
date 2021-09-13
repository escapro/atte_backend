from crm.serializers.additional_expense_category import AdditionalExpenseCategorySerializer
from rest_framework import status
from crm.models import AdditionalExpenseCategory
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser


class AdditionalExpenseCategoryView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):
        additioanl_expenses = AdditionalExpenseCategory.objects.all()
        serializer_class = AdditionalExpenseCategorySerializer(additioanl_expenses, many=True)

        return Response(serializer_class.data, status=status.HTTP_200_OK)


# class CreateAdditionalExpenseView(APIView):

#     permission_classes = (isClientUser, isAdminManager,)

#     def post(self, request):
#         serializer = ExpenseCategroyCreateSerializer(data=request.data)
        
#         if not serializer.is_valid():
#             return Response({"error_fields":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_200_OK)