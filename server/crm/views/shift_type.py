from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser
from crm.models import ShiftType
from crm.serializers.shift_type import ShiftTypeCreateSerializer, ShiftTypeSerializer


class ShiftTypeView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request):

        shift_types = ShiftType.objects.filter(
            is_active=True).order_by('index')
        serializer_class = ShiftTypeSerializer(shift_types, many=True)

        return Response(serializer_class.data)

    # def put(self, request, pk, format=None):
    #     # snippet = self.get_object(pk)
    #     # serializer = SnippetSerializer(snippet, data=request.data)
    #     # if serializer.is_valid():
    #     #     serializer.save()
    #     #     return Response(serializer.data)
    #     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     print(pk)

    #     return Response({}, status=status.HTTP_400_BAD_REQUEST)


class CreateShiftTypeView(APIView):

    permission_classes = (isClientUser, isAdminManager)

    def post(self, request, format=None):
        serializer = ShiftTypeCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({"error_fields":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)