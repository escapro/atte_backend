from crm.views.shift_type import ShiftTypeView
from crm.views.shift import ShiftView
from crm.views.expense import ExpenseView, ShiftExpensesView
from crm.views.expense_category import ExpenseCategoryView
from crm.views.admin import AdminView
from crm.views.employee import EmployeeView
from main.views.client import ClientView
from main.views.profile import ProfileView
from main.views.profile import ProfileView
from main.views.user import Logout
from django.urls import path
from django.urls.conf import include
from rest_framework.authtoken.views import obtain_auth_token

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # # path('token/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    path('auth/', include('djoser.urls')),
    path('auth/token', obtain_auth_token, name='token'),
    path('auth/logout', Logout.as_view(), name='logout'),

    path('me/', ProfileView.as_view()),
    path('clients/', ClientView.as_view()),
    path('shift_types/', ShiftTypeView.as_view()),
    path('admins/', AdminView.as_view()),
    path('employees/', EmployeeView.as_view()),
    path('expense_categories/', ExpenseCategoryView.as_view()),
    path('expenses/', ExpenseView.as_view()),
    path('admins/', AdminView.as_view()),

    path('shift_expenses/', ShiftExpensesView.as_view()),
    path('close_shift/', ShiftView.as_view()),
]