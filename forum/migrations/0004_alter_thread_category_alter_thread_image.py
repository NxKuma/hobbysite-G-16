# Generated by Django 4.2.10 on 2024-04-30 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_comment_thread_rename_postcategory_threadcategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='threads', to='forum.threadcategory'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
