from crm.serializers.expense_category import ExpenseCategroySerializer
from crm.models import ExpenseCategory
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser


class ExpenseCategoryView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        expense_categories = ExpenseCategory.objects.all()
        serializer_class = ExpenseCategroySerializer(expense_categories, many=True)

        return Response(serializer_class.data)
