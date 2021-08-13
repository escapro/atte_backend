from main.models import Admin
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
        

class Logout(APIView):
    def get(self, request, fromat=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)