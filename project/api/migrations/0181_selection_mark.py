# Generated by Django 2.1.2 on 2018-10-20 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0180_auto_20181020_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='selection',
            name='mark',
            field=models.BooleanField(default=False),
        ),
    ]