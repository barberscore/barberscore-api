# Generated by Django 2.1.8 on 2019-06-05 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmanager', '0014_auto_20190604_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='is_novice',
            field=models.BooleanField(default=False),
        ),
    ]