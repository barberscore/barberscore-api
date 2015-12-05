# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20151201_2248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='panelist',
            options={'ordering': ('panel', 'kind', 'slot')},
        ),
        migrations.AddField(
            model_name='panelist',
            name='kind',
            field=models.IntegerField(default=1, choices=[(0, b'Admin'), (1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Music Candidate'), (5, b'Presentation Candidate'), (6, b'Singing Candidate'), (7, b'Music Composite'), (8, b'Presentation Composite'), (9, b'Singing Composite')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='panelist',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='panelists', blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='panelist',
            name='panel',
            field=models.ForeignKey(related_name='panelists', to='api.Panel'),
        ),
        migrations.AlterField(
            model_name='panelist',
            name='slot',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
        migrations.AlterUniqueTogether(
            name='panelist',
            unique_together=set([('panel', 'kind', 'slot')]),
        ),
        migrations.RemoveField(
            model_name='panelist',
            name='category',
        ),
    ]
