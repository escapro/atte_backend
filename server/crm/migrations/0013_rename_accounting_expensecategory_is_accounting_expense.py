# Generated by Django 3.2.6 on 2021-09-06 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_expensecategory_accounting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expensecategory',
            old_name='accounting',
            new_name='is_accounting_expense',
        ),
    ]