# Generated by Django 5.1.3 on 2024-12-16 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0014_studentcontactproxy_studentleadproxy_alter_tag_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StudentContactProxy',
        ),
        migrations.DeleteModel(
            name='StudentLeadProxy',
        ),
    ]