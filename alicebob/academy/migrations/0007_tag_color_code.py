# Generated by Django 5.1.3 on 2024-11-25 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0006_tag_remove_historicalproduct_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color_code',
            field=models.CharField(default='#0000FF', max_length=50),
        ),
    ]
