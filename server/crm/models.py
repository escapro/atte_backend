from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import TextField
from main.models import Employee
from django.db import models


class ShiftType(models.Model):
    name = models.CharField(max_length=250, unique=True)
    index = models.IntegerField(unique=True, null=True)
    hourly_rate = models.IntegerField(unique=False, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)


class WorkingDay(models.Model):
    date = models.DateField(null=True, unique=True)
    cash_income = models.IntegerField(null=True, default=None, blank=True)
    noncash_income = models.IntegerField(null=True, default=None, blank=True)
    total_income = models.IntegerField(null=True, default=None, blank=True)
    finished = models.BooleanField(default=False,)

    def __str__(self):
        return '{}'.format(self.date)


class Cashbox(models.Model):
    name = models.CharField(max_length=500)
    index = models.IntegerField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "cashboxes"

    def __str__(self):
        return '{}'.format(self.name)


class Shift(models.Model):
    working_day = models.ForeignKey(WorkingDay, null=False, default=None, on_delete=models.CASCADE)
    shift_type = models.ForeignKey(ShiftType, null=False, default=None, on_delete=models.CASCADE)
    cashbox = models.ForeignKey(Cashbox, null=False, default=None, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, null=False, default=None, on_delete=models.CASCADE)
    cash_start = models.BigIntegerField(default=0)
    cash_end = models.BigIntegerField(default=0)
    noncash_start = models.BigIntegerField(default=0)
    noncash_end = models.BigIntegerField(default=0)
    sales = models.BigIntegerField(default=0)
    cashbox_fact = models.BigIntegerField(default=0)
    cash_refund = models.BigIntegerField(default=0)
    noncash_refund = models.BigIntegerField(default=0)
    cash_income = models.BigIntegerField(null=True, default=0)
    noncash_income = models.BigIntegerField(null=True, default=0)
    shift_income = models.BigIntegerField(null=True, default=0)
    fact = models.BooleanField(default=False)
    cash_difference = models.BigIntegerField(null=True, default=0)
    noncash_difference = models.BigIntegerField(null=True, default=0)
    difference_report = TextField(max_length=1000, null=True, default=None, blank=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.working_day.date, self.shift_type.name, self.employee.user.username, self.finished)


class WorkingTime(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    work_time = models.BigIntegerField(default=None, null=True)
    break_time = models.BigIntegerField(default=None, null=True)

    def __str__(self):
        return '{}'.format(self.shift)


class ShiftTraker(models.Model):
    START = 1
    PAUSE = 2
    RESUME = 3
    STOP = 4
    
    ACTIONS = [
        (START, 'START'),
        (PAUSE, 'PAUSE'),
        (RESUME, 'RESUME'),
        (STOP, 'STOP'),
    ]

    working_time = models.ForeignKey(WorkingTime, null=False, default=None, on_delete=models.CASCADE)
    action = models.IntegerField(choices=ACTIONS)
    datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.action not in [1,2,3,4]: raise ValueError("Недопустимое значение action={}".format(self.action))
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}, {}, {}'.format(self.working_time, self.get_action_display(), self.datetime)


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=500, unique=True)
    is_accounting_expense = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "expense categories"

    def __str__(self):
        return self.name


class Expense(models.Model):
    working_day = models.ForeignKey(WorkingDay, null=False, default=None, on_delete=models.CASCADE)
    cashbox = models.ForeignKey(Cashbox, null=False, default=None, on_delete=models.CASCADE)
    shift_type = models.ForeignKey(ShiftType, null=False, default=None, on_delete=models.CASCADE)
    expense_category = models.ForeignKey(ExpenseCategory, null=False, default=None, on_delete=models.CASCADE)
    time = models.TimeField()
    who = models.CharField(max_length=250)
    whom = models.CharField(max_length=250)
    sum = models.IntegerField()
    comment = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return '{}, {}, {}, {} - {}, {}, {}'.format(self.working_day.date, self.shift_type.name, self.expense_category, self.who, self.whom, self.sum, self.time)


class Bonuses(models.Model):
    shift_type = models.ForeignKey(ShiftType, null=False, default=None, on_delete=models.CASCADE)
    revenue_to = models.BigIntegerField(null=False)
    rate = models.IntegerField(unique=False)

    def __str__(self):
        return '{} - {}%'.format(self.revenue_to, self.rate)


class AdditionalExpenseCategory(models.Model):
    name = models.CharField(max_length=500, unique=True)

    class Meta:
        verbose_name_plural = "Additional expense categories"

    def __str__(self):
        return self.name


class AdditionalExpense(models.Model):
    date = models.DateField(null=True)
    additional_expense_category = models.ForeignKey(AdditionalExpenseCategory, null=True, default=None, on_delete=models.CASCADE, blank=True)
    name = models.TextField(max_length=500, null=True, blank=True)
    calculation_formula = models.TextField(null=True, default=None, blank=True)
    sum = models.BigIntegerField(null=True, blank=True)
    created_at_time = models.TimeField(auto_created=True, auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if self.additional_expense_category and self.name:
            raise ValueError("Недопустимое одновременно значение для name и additional_expense_category")
        if self.calculation_formula and self.sum:
            raise ValueError("Недопустимое одновременно значение для calculation_formula и sum")
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.date)


class ShiftPayrollPeriod(models.Model):
    day = models.TextField(max_length=5)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        value = self.day
        if value.isnumeric():
            value = int(value)
            if not value >= 1 and not value <= 28:
                raise ValueError("Недопустимое значение для даты. Выберите диапазон от 1 до 31")
        else:
            if value != 'end':
                print(value == 'end')
                raise ValueError("Недопустимое значение для даты. Выберите значение 'end'")
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.day)


class ShiftPayroll(models.Model):
    shift = models.ForeignKey(Shift, null=False, default=None, on_delete=models.CASCADE)
    period = models.ForeignKey(ShiftPayrollPeriod, null=False, default=None, on_delete=models.CASCADE)
    from_shift = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    from_interest = models.DecimalField(default=0, max_digits=12, decimal_places=2)


class PaidSalaries(models.Model):
    employee = models.ForeignKey(Employee, null=False, default=None, on_delete=models.CASCADE)
    date = models.DateField(default=None, null=None)
    time = models.TimeField(default=datetime.now, blank=True)
    sum = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    comment = models.TextField(max_length=500, null=True, blank=True)
