# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_auto_20151221_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(blank=True, help_text=b'\n            The objective of the contest.', null=True, choices=[(1, b'Championship'), (2, b'Qualifier')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='division',
            field=models.IntegerField(blank=True, help_text=b'\n            Detail if division/combo convention.', null=True, choices=[(200, b'Division I'), (210, b'Division II'), (220, b'Division III'), (230, b'Division IV'), (240, b'Division V'), (250, b'Arizona Division'), (260, b'NE/NW Division'), (270, b'SE/SW Division'), (280, b'Division One/Packerland Division'), (290, b'Northern Plains Division'), (300, b'10,000 Lakes and Southwest Division'), (310, b'Atlantic Division'), (320, b'Northern and Western Division'), (330, b'Southern Division'), (340, b'Sunrise Division')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='sessions', editable=False, to='api.Organization'),
        ),
    ]
