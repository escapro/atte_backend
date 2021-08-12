from crm.utils import getSubdomain
from main.models import Admin, Employee, Manager
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


class isClientUser(BasePermission):
    def has_permission(self, request, view):
        result = False
        subdomain = getSubdomain(request)
        # user_client_info = getUserClientInfo(request.user)

        if(Employee.objects.filter(user=request.user)[0].client == subdomain):
            print(Manager.objects.filter(user=request.user))
        return result

class isAdmin(BasePermission):
    def has_permission(self, request, view):
        return Admin.objects.filter(user=request.user).exists()

class isManager(BasePermission):
    def has_permission(self, request, view):
        return Manager.objects.filter(user=request.user).exists()
        
class isEmployee(BasePermission):
    def has_permission(self, request, view):
        return Employee.objects.filter(user=request.user).exists()

class isAdminManager(BasePermission):
    def has_permission(self, request, view):
        return Admin.objects.filter(user=request.user).exists() or Manager.objects.filter(user=request.user).exists()