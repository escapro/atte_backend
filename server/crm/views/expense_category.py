from rest_framework import status
from crm.serializers.expense_category import ExpenseCategroyCreateSerializer, ExpenseCategroySerializer
from crm.models import ExpenseCategory
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser


class ExpenseCategoryView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        expense_categories = ExpenseCategory.objects.all()
        serializer_class = ExpenseCategroySerializer(expense_categories, many=True)

        return Response(serializer_class.data)


class CreateExpenseCategoryView(APIView):

    permission_classes = (isClientUser, isAdminManager,)

    def post(self, request):
        serializer = ExpenseCategroyCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({"error_fields":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)