# Generated by Django 3.2.6 on 2021-10-13 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20211013_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='from_interest',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='from_shift',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
