# Generated by Django 5.0.2 on 2024-05-06 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchstore', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-created_on']},
        ),
    ]
