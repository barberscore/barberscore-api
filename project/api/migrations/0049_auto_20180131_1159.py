# Generated by Django 2.0.1 on 2018-01-31 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20180131_1146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='round',
            options={'get_latest_by': ['num']},
        ),
    ]
