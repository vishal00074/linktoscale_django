# Generated by Django 4.1.1 on 2023-07-28 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0034_rating_database_property_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prperty',
            name='Continent',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='prperty',
            name='Country',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AlterField(
            model_name='prperty',
            name='amount',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='prperty',
            name='floor_area_value',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='prperty',
            name='hide',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='prperty',
            name='image',
            field=models.ImageField(default=' ', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='prperty',
            name='site_area',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='prperty',
            name='site_area_value',
            field=models.CharField(default=' vlue', max_length=100),
        ),
        migrations.AlterField(
            model_name='prperty',
            name='title',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='prperty',
            name='user_id',
            field=models.CharField(default=' ', max_length=100),
        ),
    ]
