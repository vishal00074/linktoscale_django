# Generated by Django 4.1.1 on 2023-07-18 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0028_database'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='link',
            field=models.CharField(max_length=500),
        ),
    ]
