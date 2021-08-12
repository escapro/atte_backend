from main.views.client import ClientView
from main.views.profile import ProfileView
from crm.views.user import Logout
from crm.views.shift import ShiftView
from main.views.user import AdminListView
from django.contrib import admin
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

    path('profile/', ProfileView.as_view()),
    path('client/', ClientView.as_view()),
    path('shift/', ShiftView.as_view()),
]