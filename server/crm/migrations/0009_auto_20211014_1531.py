# Generated by Django 3.2.6 on 2021-10-14 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20211014_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shiftpayroll',
            name='date',
        ),
        migrations.RemoveField(
            model_name='shiftpayroll',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='shiftpayroll',
            name='paid',
        ),
        migrations.AddField(
            model_name='shiftpayroll',
            name='shift',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.shift'),
        ),
    ]
