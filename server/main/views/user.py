from main.permissions.user import IsAdmin
from main.models import Admin
from main.serializers import AdminSerializer
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
        

class AdminListView(generics.ListCreateAPIView):
    serializer_class = AdminSerializer
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        user = self.request.user

        print(self.request.headers)

        if user.is_authenticated:
            return Admin.objects.filter(user=user)
            
        raise PermissionDenied()

class Logout(APIView):
    def get(self, request, fromat=None):
        request.user.auth_token.delete()
        return Response(status="OK")