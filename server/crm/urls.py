from crm.views import ParametreListView
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('project_settings/all', ParametreListView.as_view()),
]