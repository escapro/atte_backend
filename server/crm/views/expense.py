from crm.serializers.expense import ExpenseCreateUpdateSerializer, ExpenseSerializer
from crm.models import Expense
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser
from rest_framework import status


class ExpenseView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        expenses = Expense.objects.all()
        serializer_class = ExpenseSerializer(expenses, many=True)

        return Response(serializer_class.data)

    def post(self, request):
        try:
            serializer = ExpenseCreateUpdateSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except BaseException as error:
            return Response({"error": "Произошла ошибка"}, status=status.HTTP_400_BAD_REQUEST)

