# Generated by Django 5.0.2 on 2024-05-08 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('0', 'open'), ('1', 'full'), ('2', 'completed'), ('3', 'discontinued')], default='0', max_length=12)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commission', to='user_management.profile')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
                ('manpower_required', models.IntegerField()),
                ('ongoing_manpower', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('0', 'open'), ('1', 'full')], default='0', max_length=4)),
                ('commission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='commissions.commission')),
            ],
            options={
                'ordering': ['status', '-manpower_required', 'role'],
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'pending'), ('1', 'accepted'), ('2', 'rejected')], default='0', max_length=8)),
                ('applied_on', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='user_management.profile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='commissions.job')),
            ],
            options={
                'ordering': ['status', '-applied_on'],
            },
        ),
    ]
