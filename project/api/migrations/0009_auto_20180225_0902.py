# Generated by Django 2.0.2 on 2018-02-25 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20180225_0857'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appearance',
            unique_together={('round', 'competitor')},
        ),
        migrations.AlterUniqueTogether(
            name='grantor',
            unique_together={('convention', 'group')},
        ),
    ]