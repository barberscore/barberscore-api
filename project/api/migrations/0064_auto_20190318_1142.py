# Generated by Django 2.1.7 on 2019-03-18 18:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_appearance_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='appearance',
            name='contesting',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, help_text='Award numbers contestanting', null=True, size=None),
        ),
        migrations.AddField(
            model_name='appearance',
            name='is_multi',
            field=models.BooleanField(default=False, help_text='If the competitor is contesting a multi-round award.'),
        ),
        migrations.AddField(
            model_name='appearance',
            name='participants',
            field=models.CharField(blank=True, default='', help_text='Director(s) or Members (listed TLBB)', max_length=255),
        ),
        migrations.AddField(
            model_name='appearance',
            name='representing',
            field=models.CharField(blank=True, default='', help_text='Representing entity', max_length=255),
        ),
    ]
