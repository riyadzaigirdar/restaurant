# Generated by Django 4.2.6 on 2023-10-21 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('employee', 'employee')], default='employee', max_length=15),
        ),
    ]
