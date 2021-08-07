# Generated by Django 3.2.6 on 2021-08-07 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_shifts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.DeleteModel(
            name='Shifts',
        ),
        migrations.AlterField(
            model_name='projectsettings',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
