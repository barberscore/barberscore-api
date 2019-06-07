# Generated by Django 2.1.8 on 2019-06-04 16:05

from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cmanager', '0007_auto_20190603_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='location',
            field=models.CharField(blank=True, default='', help_text='\n            The location in the form "City, State".', max_length=255),
        ),
        migrations.AlterField(
            model_name='convention',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(blank=True, help_text='\n            The local timezone of the convention.', null=True),
        ),
    ]