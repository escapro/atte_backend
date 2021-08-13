from main.serializers.admin import AdminSerializer
from main.models import Admin
from crm.utils import getSubdomain, getUserClientInfo
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdmin, isClientUser


class AdminView(APIView):

    # permission_classes = (isClientUser)

    def get(self, request):

        admins = Admin.objects.all()
        serializer_class = AdminSerializer(admins, many=True)

        return Response(serializer_class.data)
