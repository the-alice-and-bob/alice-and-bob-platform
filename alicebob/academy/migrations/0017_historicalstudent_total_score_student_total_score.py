# Generated by Django 5.1.3 on 2024-12-16 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0016_historicalproduct_engagement_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudent',
            name='total_score',
            field=models.FloatField(default=0, help_text='Score total del estudiante.'),
        ),
        migrations.AddField(
            model_name='student',
            name='total_score',
            field=models.FloatField(default=0, help_text='Score total del estudiante.'),
        ),
    ]
