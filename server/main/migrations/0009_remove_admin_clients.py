# Generated by Django 3.2.6 on 2021-08-13 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210813_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='clients',
        ),
    ]