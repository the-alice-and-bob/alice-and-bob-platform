# Generated by Django 5.1.3 on 2024-12-10 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_maillist_dailyemail_mail_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyemail',
            name='is_sent',
        ),
    ]
