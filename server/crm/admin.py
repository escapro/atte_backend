from crm.models import *
from django.contrib import admin

# Register your models here.
admin.site.register(ShiftType)
admin.site.register(ExpenseCategory)
admin.site.register(Expense)
admin.site.register(ShiftTraker)
admin.site.register(Cashbox)
admin.site.register(Bonuses)
admin.site.register(AdditionalExpenseCategory)
admin.site.register(AdditionalExpense)
admin.site.register(WorkingTime)
admin.site.register(ShiftPayrollPeriod)
admin.site.register(ShiftPayroll)


@admin.register(WorkingDay)
class WorkingDay(admin.ModelAdmin):
    readonly_fields = [
        'cash_income',
        'noncash_income',
        'total_income',
    ]


@admin.register(Shift)
class Shift(admin.ModelAdmin):
    readonly_fields = [
        'cash_income',
        'noncash_income',
        'shift_income',
        'fact',
        'cash_difference',
        'noncash_difference',
        'difference_report'
    ]