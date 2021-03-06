# Generated by Django 3.2.6 on 2021-11-17 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '__first__'),
        ('crm', '0011_auto_20211022_2217'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishesDailyShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=None)),
                ('employee', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.employee')),
                ('shift_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.shifttype')),
            ],
        ),
        migrations.CreateModel(
            name='DailyShiftSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=None)),
                ('employee', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.employee')),
                ('shift_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.shifttype')),
            ],
        ),
    ]
