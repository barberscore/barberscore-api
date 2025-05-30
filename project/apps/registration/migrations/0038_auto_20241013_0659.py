# Generated by Django 2.2.27 on 2024-10-13 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0037_auto_20240706_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='district',
            field=models.IntegerField(blank=True, choices=[('BHS', [(200, 'CAR'), (205, 'CSD'), (210, 'SHD'), (215, 'EVG'), (220, 'FWD'), (225, 'ILL'), (230, 'JAD'), (235, 'LOL'), (240, 'MAD'), (345, 'NED'), (350, 'NSC'), (355, 'ONT'), (360, 'PIO'), (365, 'RMD'), (370, 'SLD'), (375, 'SUN'), (380, 'SWD')]), ('Associated', [(410, 'NxtGn'), (420, 'MBHA'), (430, 'HI'), (700, 'AREA1'), (705, 'AREA2'), (710, 'AREA3'), (715, 'AREA4'), (720, 'AREA5'), (725, 'AREA6'), (440, 'SAI')]), ('Affiliated', [(510, 'BABS'), (515, 'BHA'), (750, 'VR'), (755, 'WR'), (760, 'CR'), (765, 'ER'), (770, 'SR'), (775, 'TR'), (520, 'BHNZ'), (800, 'NR'), (805, 'CR'), (810, 'SR'), (525, 'BinG!'), (530, 'FABS'), (540, 'HHar'), (550, 'IABS'), (560, 'LABBS'), (565, 'BIBA'), (570, 'SNOBS'), (575, 'SPATS')])], null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='district',
            field=models.IntegerField(blank=True, choices=[(110, 'BHS'), (200, 'CAR'), (205, 'CSD'), (210, 'SHD'), (215, 'EVG'), (220, 'FWD'), (225, 'ILL'), (230, 'JAD'), (235, 'LOL'), (240, 'MAD'), (345, 'NED'), (350, 'NSC'), (355, 'ONT'), (360, 'PIO'), (365, 'RMD'), (370, 'SLD'), (375, 'SUN'), (380, 'SWD'), (430, 'HI'), (510, 'BABS'), (515, 'BHA'), (520, 'BHNZ'), (525, 'BinG!'), (530, 'FABS'), (540, 'HHar'), (550, 'IABS'), (560, 'LABBS'), (565, 'BIBA'), (570, 'SNOBS'), (575, 'SPATS'), (700, 'AREA1'), (705, 'AREA2'), (710, 'AREA3'), (715, 'AREA4'), (720, 'AREA5'), (725, 'AREA6'), (750, 'VR'), (755, 'WR'), (760, 'CR'), (765, 'ER'), (770, 'SR'), (775, 'TR'), (800, 'NR'), (805, 'CR'), (810, 'SR')], null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='district',
            field=models.IntegerField(blank=True, choices=[('BHS', [(200, 'CAR'), (205, 'CSD'), (210, 'SHD'), (215, 'EVG'), (220, 'FWD'), (225, 'ILL'), (230, 'JAD'), (235, 'LOL'), (240, 'MAD'), (345, 'NED'), (350, 'NSC'), (355, 'ONT'), (360, 'PIO'), (365, 'RMD'), (370, 'SLD'), (375, 'SUN'), (380, 'SWD')]), ('Associated', [(410, 'NxtGn'), (420, 'MBHA'), (430, 'HI'), (700, 'AREA1'), (705, 'AREA2'), (710, 'AREA3'), (715, 'AREA4'), (720, 'AREA5'), (725, 'AREA6'), (440, 'SAI')]), ('Affiliated', [(510, 'BABS'), (515, 'BHA'), (750, 'VR'), (755, 'WR'), (760, 'CR'), (765, 'ER'), (770, 'SR'), (775, 'TR'), (520, 'BHNZ'), (800, 'NR'), (805, 'CR'), (810, 'SR'), (525, 'BinG!'), (530, 'FABS'), (540, 'HHar'), (550, 'IABS'), (560, 'LABBS'), (565, 'BIBA'), (570, 'SNOBS'), (575, 'SPATS')])], null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='district',
            field=models.IntegerField(blank=True, choices=[(110, 'BHS'), (200, 'CAR'), (205, 'CSD'), (210, 'SHD'), (215, 'EVG'), (220, 'FWD'), (225, 'ILL'), (230, 'JAD'), (235, 'LOL'), (240, 'MAD'), (345, 'NED'), (350, 'NSC'), (355, 'ONT'), (360, 'PIO'), (365, 'RMD'), (370, 'SLD'), (375, 'SUN'), (380, 'SWD'), (430, 'HI'), (510, 'BABS'), (515, 'BHA'), (520, 'BHNZ'), (525, 'BinG!'), (530, 'FABS'), (540, 'HHar'), (550, 'IABS'), (560, 'LABBS'), (565, 'BIBA'), (570, 'SNOBS'), (575, 'SPATS'), (700, 'AREA1'), (705, 'AREA2'), (710, 'AREA3'), (715, 'AREA4'), (720, 'AREA5'), (725, 'AREA6'), (750, 'VR'), (755, 'WR'), (760, 'CR'), (765, 'ER'), (770, 'SR'), (775, 'TR'), (800, 'NR'), (805, 'CR'), (810, 'SR')], null=True),
        ),
    ]
