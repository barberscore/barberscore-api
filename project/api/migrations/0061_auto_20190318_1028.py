# Generated by Django 2.1.7 on 2019-03-18 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0060_auto_20190318_1025'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appearance',
            unique_together={('round', 'competitor'), ('round', 'num'), ('round', 'group')},
        ),
    ]
