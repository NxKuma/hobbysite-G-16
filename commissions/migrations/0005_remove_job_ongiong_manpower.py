# Generated by Django 5.0.2 on 2024-05-03 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0004_alter_job_commission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='ongiong_manpower',
        ),
    ]