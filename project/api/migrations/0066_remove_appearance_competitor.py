# Generated by Django 2.1.7 on 2019-03-18 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0065_auto_20190318_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appearance',
            name='competitor',
        ),
    ]
