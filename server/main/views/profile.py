from crm.permissions import isClientUser
from crm.utils.common import getUserClientInfo
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.utils.common import getUserClientInfo


class ProfileView(APIView):

    permission_classes = (isClientUser,)

    def get(self, request, format=None):

        data = {}
        data['username'] = request.user.username
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name
        data['email'] = request.user.email

        user_client_info = getUserClientInfo(request.user)

        data['role'] = user_client_info['role']
        data['client'] = user_client_info['client']

        return Response(data)
