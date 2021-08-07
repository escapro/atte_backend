from main.models import Client, Employee
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    tenant = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return "Project: {}".format(self.tenant)


class Parametre(models.Model):
    name = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=False, default='') 
    def __str__(self):
        return "{}:{}".format(self.name, self.value)


class Shift(models.Model):
    SHIFT_TYPES = [
        ('1', 'Утро'),
        ('2', 'День'),
        ('3', 'Ночь'),
    ]
    shift_type = models.CharField(choices=SHIFT_TYPES, default=1, unique=True, max_length=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.shift_type

class WorkingDay(models.Model):
    date = models.DateField(unique=True)
    def __str__(self):
        return str(self.date)