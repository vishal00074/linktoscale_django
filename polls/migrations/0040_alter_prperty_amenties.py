# Generated by Django 4.2.5 on 2023-09-08 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0039_alter_rating_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prperty',
            name='amenties',
            field=models.CharField(max_length=1000),
        ),
    ]
