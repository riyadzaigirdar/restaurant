# Generated by Django 4.2.6 on 2023-10-21 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_menumodel_name_alter_menumodel_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantmodel',
            name='location',
            field=models.TextField(null=True),
        ),
    ]
