# Generated by Django 4.2.6 on 2023-10-21 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_menumodel_restaurantmodel_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menumodel',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='menumodel',
            name='name',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='menumodel',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='menumodel',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurantmodel'),
        ),
        migrations.AlterField(
            model_name='menumodel',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='RecipeModel',
        ),
    ]
