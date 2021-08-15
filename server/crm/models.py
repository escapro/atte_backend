from enum import unique
from main.models import Employee
from django.db import models
import datetime


class ShiftType(models.Model):
    name = models.CharField(max_length=250, unique=True)
    index = models.IntegerField(unique=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)


class WorkingDay(models.Model):
    date = models.DateField(null=True)
    shifts_left = models.IntegerField(unique=True, null=False)
    cash_income = models.IntegerField(null=True)
    noncash_income = models.IntegerField(null=True)

    def __str__(self):
        return '{}'.format(self.date)


class Shift(models.Model):
    working_day = models.ForeignKey(
        WorkingDay, null=False, default=None, on_delete=models.CASCADE)
    shift_type = models.ForeignKey(
        ShiftType, null=False, default=None, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Employee, null=False, default=None, on_delete=models.CASCADE)
    shift_start_time = models.TimeField()
    shift_end_time = models.TimeField()
    cash_start = models.IntegerField()
    cash_end = models.IntegerField()
    noncash_start = models.IntegerField()
    noncash_end = models.IntegerField()
    sales = models.IntegerField()
    cashbox_fact = models.IntegerField()
    refund = models.IntegerField()
    cash_income = models.IntegerField(null=True)
    noncash_income = models.IntegerField(null=True)
    shift_income = models.IntegerField(null=True)
    fact = models.BooleanField(default=False)
    cash_difference = models.IntegerField(null=True)
    noncash_difference = models.IntegerField(null=True)

    def __str__(self):
        return '{}, {}, {} - {}'.format(self.shift_type.name, self.employee.user.username, self.shift_start_time, self.shift_end_time)


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    working_day = models.ForeignKey(
        WorkingDay, null=False, default=None, on_delete=models.CASCADE)
    shift_type = models.ForeignKey(
        ShiftType, null=False, default=None, on_delete=models.CASCADE)
    expense_category = models.ForeignKey(
        ExpenseCategory, null=False, default=None, on_delete=models.CASCADE)
    time = models.TimeField()
    who = models.CharField(max_length=250)
    whom = models.CharField(max_length=250)
    sum = models.IntegerField()
    comment = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return '{}, {}, {} - {}, {}, {}'.format(self.shift_type.name, self.expense_category, self.who, self.whom, self.sum, self.time)
