# Generated by Django 5.0.2 on 2024-05-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0002_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='ongiong_manpower',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='job',
            name='open_manpower',
            field=models.IntegerField(default=0),
        ),
    ]
