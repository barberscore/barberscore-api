# Generated by Django 2.2.27 on 2022-05-30 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0027_auto_20220322_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='category',
            field=models.IntegerField(blank=True, choices=[(5, 'DRCJ'), (10, 'ADM'), (30, 'Music'), (40, 'Performance'), (50, 'Singing')], null=True),
        ),
    ]
