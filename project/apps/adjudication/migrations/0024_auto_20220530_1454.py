# Generated by Django 2.2.27 on 2022-05-30 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adjudication', '0023_auto_20220411_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panelist',
            name='category',
            field=models.IntegerField(blank=True, choices=[(5, 'DRCJ'), (10, 'ADM'), (30, 'Music'), (40, 'Performance'), (50, 'Singing')], null=True),
        ),
    ]
