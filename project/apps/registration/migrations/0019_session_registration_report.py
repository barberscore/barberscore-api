# Generated by Django 2.2.5 on 2019-09-17 21:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0018_auto_20190917_0644'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='registration_report',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
