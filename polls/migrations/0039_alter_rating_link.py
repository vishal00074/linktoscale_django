# Generated by Django 4.1.1 on 2023-08-04 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0038_rating_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='link',
            field=models.CharField(default='', max_length=500),
        ),
    ]
