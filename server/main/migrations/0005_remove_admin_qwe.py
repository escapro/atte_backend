# Generated by Django 3.2.6 on 2021-08-13 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_admin_qwe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='qwe',
        ),
    ]