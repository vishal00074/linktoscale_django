# Generated by Django 4.2.5 on 2023-11-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0052_alter_database_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='expired_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
