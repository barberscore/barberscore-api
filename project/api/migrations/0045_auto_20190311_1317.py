# Generated by Django 2.1.7 on 2019-03-11 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20190307_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='outcome',
            name='advance',
            field=models.FloatField(blank=True, help_text='\n            The score threshold to advance to next round (if any) in\n            multi-round qualification.\n        ', null=True),
        ),
        migrations.AddField(
            model_name='outcome',
            name='level',
            field=models.IntegerField(choices=[(10, 'Championship'), (30, 'Qualifier'), (45, 'Representative'), (50, 'Deferred'), (60, 'Manual'), (70, 'Improved - Raw'), (80, 'Improved - Standard')], null=True),
        ),
        migrations.AddField(
            model_name='outcome',
            name='minimum',
            field=models.FloatField(blank=True, help_text='\n            The minimum score required for qualification (if any.)\n        ', null=True),
        ),
        migrations.AddField(
            model_name='outcome',
            name='num_rounds',
            field=models.IntegerField(help_text='Number of rounds to determine the championship', null=True),
        ),
        migrations.AddField(
            model_name='outcome',
            name='spots',
            field=models.IntegerField(blank=True, help_text='Number of top spots which qualify', null=True),
        ),
        migrations.AddField(
            model_name='outcome',
            name='threshold',
            field=models.FloatField(blank=True, help_text='\n            The score threshold for automatic qualification (if any.)\n        ', null=True),
        ),
    ]