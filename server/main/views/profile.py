from crm.utils import getUserClientInfo
from rest_framework.response import Response
from rest_framework.views import APIView


class ProfileView(APIView):
    def get(self, request, format=None):

        data = {}
        data['username'] = request.user.username
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
        data['email'] = request.user.email

        user_client_info = getUserClientInfo(request.user)

        data['role'] = user_client_info['role']
        data['clients'] = user_client_info['clients']

        return Response(data)
