# Generated by Django 3.2.6 on 2021-08-17 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0016_auto_20210817_1954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workingday',
            old_name='revenue',
            new_name='total_income',
        ),
    ]
