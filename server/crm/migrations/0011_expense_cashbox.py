# Generated by Django 3.2.6 on 2021-09-01 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_auto_20210901_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='cashbox',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.cashbox'),
        ),
    ]