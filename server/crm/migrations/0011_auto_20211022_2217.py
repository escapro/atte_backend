# Generated by Django 3.2.6 on 2021-10-22 22:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_paidsalaries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paidsalaries',
            name='datetime',
        ),
        migrations.AddField(
            model_name='paidsalaries',
            name='date',
            field=models.DateField(default=None, null=None),
        ),
        migrations.AddField(
            model_name='paidsalaries',
            name='time',
            field=models.TimeField(blank=True, default=datetime.datetime.now),
        ),
    ]