# Generated by Django 5.1.3 on 2024-11-25 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0009_alter_historicalproduct_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproduct',
            name='extra_data',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='zoho_tags',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='extra_data',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='zoho_tags',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
