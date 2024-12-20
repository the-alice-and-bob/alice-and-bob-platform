# Generated by Django 5.1.3 on 2024-11-25 14:33

import academy.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0004_courseprogress_zoho_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='extra_data',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='image',
            field=models.URLField(default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='language',
            field=models.CharField(default='Español', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='published_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='created_date',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='user_status',
            field=models.CharField(choices=[(academy.models.UserStatus['ACTIVE'], 'ACTIVE'), (academy.models.UserStatus['INACTIVE'], 'INACTIVE'), (academy.models.UserStatus['SUSPENDED'], 'SUSPENDED'), (academy.models.UserStatus['DELETED'], 'DELETED')], default=academy.models.UserStatus['ACTIVE'], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='historicalstudent',
            name='user_type',
            field=models.CharField(choices=[(academy.models.UserType['STUDENT'], 'student'), (academy.models.UserType['TEACHER'], 'teacher'), (academy.models.UserType['ADMIN'], 'admin')], default=academy.models.UserType['STUDENT'], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='extra_data',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.URLField(default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='language',
            field=models.CharField(default='Español', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='published_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='user_status',
            field=models.CharField(choices=[(academy.models.UserStatus['ACTIVE'], 'ACTIVE'), (academy.models.UserStatus['INACTIVE'], 'INACTIVE'), (academy.models.UserStatus['SUSPENDED'], 'SUSPENDED'), (academy.models.UserStatus['DELETED'], 'DELETED')], default=academy.models.UserStatus['ACTIVE'], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='user_type',
            field=models.CharField(choices=[(academy.models.UserType['STUDENT'], 'student'), (academy.models.UserType['TEACHER'], 'teacher'), (academy.models.UserType['ADMIN'], 'admin')], default=academy.models.UserType['STUDENT'], max_length=50, null=True),
        ),
    ]
