# Generated by Django 2.1.3 on 2018-11-21 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0206_auto_20181120_1852'),
    ]

    operations = [
        migrations.RenameField(
            model_name='award',
            old_name='divizion',
            new_name='division',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='divizion',
            new_name='division',
        ),
    ]
