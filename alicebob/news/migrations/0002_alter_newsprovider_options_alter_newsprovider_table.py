# Generated by Django 5.1.3 on 2024-11-26 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsprovider',
            options={'verbose_name': 'Provider', 'verbose_name_plural': 'Providers'},
        ),
        migrations.AlterModelTable(
            name='newsprovider',
            table='news_providers',
        ),
    ]
