# Generated by Django 3.2.6 on 2021-10-11 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('from_shift', models.BigIntegerField(default=0)),
                ('from_interest', models.BigIntegerField(default=0)),
                ('paid', models.BigIntegerField(default=0)),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.payrollperiod')),
            ],
        ),
    ]
