# Generated by Django 2.1.2 on 2018-10-17 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0156_auto_20181017_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flat',
            name='convention',
        ),
        migrations.RemoveField(
            model_name='flat',
            name='panelist',
        ),
        migrations.RemoveField(
            model_name='flat',
            name='round',
        ),
        migrations.RemoveField(
            model_name='flat',
            name='session',
        ),
        migrations.DeleteModel(
            name='Flat',
        ),
    ]