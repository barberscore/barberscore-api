# Generated by Django 2.0.8 on 2018-09-04 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0102_auto_20180904_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bhs_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]