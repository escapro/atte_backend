# Generated by Django 3.2.6 on 2021-08-16 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20210815_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingday',
            name='date',
            field=models.DateField(null=True, unique=True),
        ),
    ]
