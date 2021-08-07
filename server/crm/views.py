from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.serializers import Serializer
from crm.models import Parametre
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from .serializers import *

class Logout(APIView):

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ParametreListView(generics.ListAPIView):
    queryset = Parametre.objects.all()
    serializer_class = ParametreSerializer
    permission_classes = [permissions.IsAuthenticated]