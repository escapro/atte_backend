# Generated by Django 3.2.6 on 2021-08-07 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='name',
        ),
        migrations.AlterField(
            model_name='project',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.client'),
        ),
        migrations.CreateModel(
            name='ProjectSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('tenant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.client')),
            ],
        ),
    ]
