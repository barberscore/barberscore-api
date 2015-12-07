# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20151206_2301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ('round', 'position')},
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='session',
            new_name='round',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='rounds',
        ),
        migrations.AddField(
            model_name='contest',
            name='num_rounds',
            field=models.IntegerField(default=1, help_text=b'\n            Number of rounds (rounds) for the contest.', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='award',
            name='rounds',
            field=models.IntegerField(help_text=b'\n            The number of rounds that will be used in determining the award.  Note that this may be fewer than the total number of rounds (rounds) in the parent contest.', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final ranking relative to this round.', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='contest',
            field=models.ForeignKey(related_name='rounds', to='api.Contest'),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('round', 'contestant')]),
        ),
    ]
