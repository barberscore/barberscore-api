# Generated by Django 2.2.20 on 2021-10-06 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0024_auto_20210929_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='kind',
            field=models.IntegerField(choices=[(-10, 'Former'), (10, 'Official'), (20, 'Practice')]),
        ),
    ]