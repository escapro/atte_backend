# Generated by Django 3.2.6 on 2021-09-11 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0017_additionalexpense_additionalexpensecategory_calculationformula'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionalexpensecategory',
            name='is_accounting_expense',
        ),
    ]
