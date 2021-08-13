from crm.utils import getSubdomain, getUserClientInfo
from main.models import Admin, Employee, Manager
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


class isClientUser(BasePermission):
    def has_permission(self, request, view):
        if(request.user.is_anonymous):
            return False

        subdomain = getSubdomain(request)
        user_client_info = getUserClientInfo(request.user)
        
        if(subdomain in user_client_info['clients']):
            return True

        return False

class isAdmin(BasePermission):
    def has_permission(self, request, view):
        if(request.user.is_anonymous):
            return False
        return Admin.objects.filter(user=request.user).exists()

class isManager(BasePermission):
    def has_permission(self, request, view):
        if(request.user.is_anonymous):
            return False
        return Manager.objects.filter(user=request.user).exists()
        
class isEmployee(BasePermission):
    def has_permission(self, request, view):
        if(request.user.is_anonymous):
            return False
        return Employee.objects.filter(user=request.user).exists()

class isAdminManager(BasePermission):
    def has_permission(self, request, view):
        if(request.user.is_anonymous):
            return False
        return Admin.objects.filter(user=request.user).exists() or Manager.objects.filter(user=request.user).exists()