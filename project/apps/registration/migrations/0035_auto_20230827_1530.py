# Generated by Django 2.2.27 on 2023-08-27 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0034_auto_20230827_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='district',
            field=models.IntegerField(blank=True, choices=[(110, 'BHS'), (200, 'CAR'), (205, 'CSD'), (210, 'DIX'), (215, 'EVG'), (220, 'FWD'), (225, 'ILL'), (230, 'JAD'), (235, 'LOL'), (240, 'MAD'), (345, 'NED'), (350, 'NSC'), (355, 'ONT'), (360, 'PIO'), (365, 'RMD'), (370, 'SLD'), (375, 'SUN'), (380, 'SWD'), (430, 'HI')], null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='district',
            field=models.IntegerField(blank=True, choices=[(110, 'BHS'), (200, 'CAR'), (205, 'CSD'), (210, 'DIX'), (215, 'EVG'), (220, 'FWD'), (225, 'ILL'), (230, 'JAD'), (235, 'LOL'), (240, 'MAD'), (345, 'NED'), (350, 'NSC'), (355, 'ONT'), (360, 'PIO'), (365, 'RMD'), (370, 'SLD'), (375, 'SUN'), (380, 'SWD'), (430, 'HI')], null=True),
        ),
    ]
