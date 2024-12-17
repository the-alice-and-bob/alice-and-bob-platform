# Generated by Django 5.1.4 on 2024-12-17 13:10

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0018_alter_historicalproduct_product_type_and_more'),
        ('campaigns', '0010_alter_maillist_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyemail',
            name='acumbamail_id',
            field=models.IntegerField(blank=True, db_index=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='dailyemail',
            name='total_bounces',
            field=models.IntegerField(default=0, help_text='Total de rebotes registrados en esta campaña.'),
        ),
        migrations.AddField(
            model_name='dailyemail',
            name='total_clicks',
            field=models.IntegerField(default=0, help_text='Total de clics registrados en esta campaña.'),
        ),
        migrations.AddField(
            model_name='dailyemail',
            name='total_complaints',
            field=models.IntegerField(default=0, help_text='Total de quejas registradas en esta campaña.'),
        ),
        migrations.AddField(
            model_name='dailyemail',
            name='total_opens',
            field=models.IntegerField(default=0, help_text='Total de emails abiertos en esta campaña.'),
        ),
        migrations.AddField(
            model_name='dailyemail',
            name='total_sent',
            field=models.IntegerField(default=0, help_text='Total de emails enviados en esta campaña.'),
        ),
        migrations.AddField(
            model_name='dailyemail',
            name='total_unsubscribes',
            field=models.IntegerField(default=0, help_text='Total de de-suscripciones registradas en esta campaña.'),
        ),
        migrations.AlterModelTable(
            name='dailyemail',
            table='daily_email',
        ),
        migrations.CreateModel(
            name='EmailEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('email', models.EmailField(help_text='Email asociado al evento.', max_length=800)),
                ('event_type', models.CharField(choices=[('open', 'OPEN'), ('click', 'CLICK'), ('complaint', 'COMPLAINT'), ('hard_bounce', 'HARD_BOUNCE'), ('soft_bounce', 'SOFT_BOUNCE'), ('delivered', 'DELIVERED'), ('unsubscribe', 'UNSUBSCRIBE'), ('subscribe', 'SUBSCRIBE')], help_text='Tipo de evento registrado para este email.', max_length=50)),
                ('timestamp', models.DateTimeField(help_text='Fecha y hora del evento.')),
                ('metadata', models.JSONField(blank=True, default=dict, help_text='Información adicional sobre el evento en formato JSON.')),
                ('campaign', models.ForeignKey(blank=True, help_text='Email que disparó este evento.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_events', to='campaigns.dailyemail')),
                ('student', models.ForeignKey(blank=True, help_text='Estudiante relacionado al evento (si corresponde).', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_events', to='academy.student')),
            ],
            options={
                'verbose_name': 'Email Event',
                'verbose_name_plural': 'Email Events',
                'db_table': 'email_event',
            },
        ),
    ]
