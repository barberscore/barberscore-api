# Generated by Django 2.1.7 on 2019-03-11 22:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_remove_competitor_contesting'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='contesting',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, help_text='Award numbers contestanting', null=True, size=None),
        ),
    ]
