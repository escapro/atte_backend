# Generated by Django 3.2.6 on 2021-08-13 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_admin_clients'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='clients',
            field=models.ManyToManyField(blank=True, to='main.Client'),
        ),
    ]