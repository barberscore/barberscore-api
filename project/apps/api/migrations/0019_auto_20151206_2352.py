# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20151206_2350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('contest', 'performer')},
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='award',
            new_name='contest',
        ),
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(help_text=b'\n            The objective of the contest.', choices=[(1, b'Championship'), (2, b'Qualifier')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of the contest.  Note that this may be different than the kind of the parent session.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (5, b'Novice'), (6, b'Plateau A'), (7, b'Plateau AA'), (8, b'Plateau AAA'), (9, b"Dealer's Choice")]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(help_text=b'\n            The level of the contest.  Note that this may be different than the level of the parent session.', choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='contests', to='api.Organization', help_text=b'\n            The organization that will confer the contest.  Note that this may be different than the organization running the parent session.'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='qual_score',
            field=models.FloatField(help_text=b'\n            The objective of the contest.  Note that if the goal is `qualifier` then this must be set.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='rounds',
            field=models.IntegerField(help_text=b'\n            The number of rounds that will be used in determining the contest.  Note that this may be fewer than the total number of rounds (rounds) in the parent session.', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='session',
            field=models.ForeignKey(related_name='contests', to='api.Session'),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final ranking relative to this contest.', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performer',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final placement/rank of the performer for the entire session (ie, not a specific contest).', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='points',
            field=models.IntegerField(blank=True, help_text=b'\n            The number of points contested (0-100)', null=True, validators=[django.core.validators.MaxValueValidator(100, message=b'Points must be between 0 - 100'), django.core.validators.MinValueValidator(0, message=b'Points must be between 0 - 100')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='sessions', editable=False, to='api.Organization', help_text=b'\n            The organization that will confer the contest.  Note that this may be different than the organization running the parent session.'),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('performer', 'contest')]),
        ),
    ]
