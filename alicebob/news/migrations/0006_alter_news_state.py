# Generated by Django 5.1.3 on 2024-11-28 14:48

import news.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_remove_channelpublication_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='state',
            field=models.CharField(choices=[('BACKLOG', 'BACKLOG'), ('DRAFT', 'DRAFT'), ('PUBLISHED', 'PUBLISHED'), ('ARCHIVED', 'ARCHIVED'), ('REVIEW', 'REVIEW')], default=news.models.NewsState['BACKLOG'], max_length=40),
        ),
    ]