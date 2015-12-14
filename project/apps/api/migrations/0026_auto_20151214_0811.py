# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20151213_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='subsession_text',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='division',
            field=models.IntegerField(blank=True, help_text=b'\n            This is a division convention of Divisions.', null=True, choices=[(200, b'Division I'), (210, b'Division II'), (220, b'Division III'), (230, b'Division IV'), (240, b'Division V'), (250, b'Arizona Division'), (260, b'NE/NW Division'), (270, b'SE/SW Division'), (280, b'Division One/Packerland Division'), (290, b'Northern Plains Division'), (300, b'10,000 Lakes and Southwest Division'), (310, b'Atlantic Division'), (320, b'Northern and Western Division'), (330, b'Southern Division'), (340, b'Sunrise Division')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of convention.', choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (9, b'Video')]),
        ),
        migrations.AlterUniqueTogether(
            name='convention',
            unique_together=set([('organization', 'kind', 'year', 'division')]),
        ),
    ]
