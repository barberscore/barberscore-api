# Generated by Django 2.1.8 on 2019-05-28 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20190528_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appearance',
            name='legacy_num',
        ),
        migrations.RemoveField(
            model_name='song',
            name='legacy_group',
        ),
        migrations.AddField(
            model_name='appearance',
            name='legacy_group',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
