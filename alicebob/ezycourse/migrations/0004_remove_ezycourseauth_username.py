# Generated by Django 5.1.3 on 2024-11-25 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ezycourse', '0003_remove_ezycourseauth_ezycourse_a_access__8b5149_idx_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ezycourseauth',
            name='username',
        ),
    ]
