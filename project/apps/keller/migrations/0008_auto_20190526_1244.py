# Generated by Django 2.1.8 on 2019-05-26 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keller', '0007_auto_20190526_0727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rawpanelist',
            old_name='points',
            new_name='scores',
        ),
    ]
