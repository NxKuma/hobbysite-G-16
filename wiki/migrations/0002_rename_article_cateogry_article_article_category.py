# Generated by Django 4.2.10 on 2024-03-20 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article_cateogry',
            new_name='article_category',
        ),
    ]