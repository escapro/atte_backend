from crm.views.additional_expense_category import AdditionalExpenseCategoryView
from crm.views.additional_expense import AdditionalExpenseView, CreateAdditionalExpenseView
from crm.views.bonuse import BonuseView, CreateBonuseView
from crm.views.accounting import AccountingView
from crm.views.cashbox import CashboxView
from crm.views.paid_salary import PaidSalaryView, CreatePaidSalaryView
from crm.views.payroll import PayrollView
from crm.views.working_day import CloseWdView
from crm.views.shift_type import CreateShiftTypeView, ShiftTypeView
from crm.views.shift import ActiveShiftView, CheckShiftView, CloseShiftView, OpenShiftView
from crm.views.expense import ExpenseView, ShiftExpensesView
from crm.views.expense_category import CreateExpenseCategoryView, ExpenseCategoryView
from crm.views.admin import AdminView
from crm.views.employee import CreateEmployeeView, EmployeeView
from main.views.client import ClientView, UpdateClientView
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
    path('client/update', UpdateClientView.as_view()),

    path('shift_types/', ShiftTypeView.as_view()),
    path('shift_type/new/', CreateShiftTypeView.as_view()),

    path('cashboxes/', CashboxView.as_view()),
    path('admins/', AdminView.as_view()),

    path('employees/', EmployeeView.as_view()),
    path('employee/new/', CreateEmployeeView.as_view()),

    path('expense_categories/', ExpenseCategoryView.as_view()),
    path('expense_categorie/new/', CreateExpenseCategoryView.as_view()),

    path('expenses/', ExpenseView.as_view()),
    path('admins/', AdminView.as_view()),

    # path('check_shift/', CheckShiftView.as_view()),
    path('shifts/check/', CheckShiftView.as_view()),
    path('shifts/open/', OpenShiftView.as_view()),
    path('shifts/active/', ActiveShiftView.as_view()),
    path('shifts/active/close', CloseShiftView.as_view()),

    path('working_day/active/close', CloseWdView.as_view()),

    path('shift_expenses/', ShiftExpensesView.as_view()),

    path('accounting/', AccountingView.as_view()),

    path('bonuses/', BonuseView.as_view()),
    path('bonuse/new/', CreateBonuseView.as_view()),

    path('additional_expenses/', AdditionalExpenseView.as_view()),
    path('additional_expense/new/', CreateAdditionalExpenseView.as_view()),

    path('additional_expense_categories/', AdditionalExpenseCategoryView.as_view()),
    # path('additional_expense/new/', CreateExpenseCategoryView.as_view()),

    path('payrolls/', PayrollView.as_view()),

    path('paid_salaries/', PaidSalaryView.as_view()),
    path('paid_salary/new/', CreatePaidSalaryView.as_view()),
    
]