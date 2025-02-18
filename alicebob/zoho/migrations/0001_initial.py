# Generated by Django 5.1.3 on 2024-11-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ZohoOAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=255, unique=True)),
                ('client_secret', models.CharField(max_length=255, unique=True)),
                ('grant_token', models.CharField(max_length=255, unique=True)),
                ('refresh_token', models.CharField(max_length=255, unique=True)),
                ('access_token', models.CharField(max_length=255, unique=True)),
                ('expiry_time', models.IntegerField()),
                ('api_domain', models.CharField(max_length=255)),
                ('redirect_uri', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Zoho OAuth',
                'verbose_name_plural': 'Zoho OAuth',
                'db_table': 'zoho_oauth',
                'indexes': [models.Index(fields=['access_token', 'refresh_token'], name='zoho_oauth_access__3ba2de_idx')],
            },
        ),
    ]
