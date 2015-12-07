# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20151206_2321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('session', 'group')},
        ),
        migrations.AlterModelOptions(
            name='judge',
            options={'ordering': ('session', 'kind', 'category', 'slot')},
        ),
        migrations.AlterModelOptions(
            name='round',
            options={'ordering': ('session', 'kind')},
        ),
        migrations.RenameField(
            model_name='award',
            old_name='contest',
            new_name='session',
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='contest',
            new_name='session',
        ),
        migrations.RenameField(
            model_name='judge',
            old_name='contest',
            new_name='session',
        ),
        migrations.RenameField(
            model_name='round',
            old_name='contest',
            new_name='session',
        ),
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of the award.  Note that this may be different than the kind of the parent session.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (5, b'Novice'), (6, b'Plateau A'), (7, b'Plateau AA'), (8, b'Plateau AAA'), (9, b"Dealer's Choice")]),
        ),
        migrations.AlterField(
            model_name='award',
            name='level',
            field=models.IntegerField(help_text=b'\n            The level of the award.  Note that this may be different than the level of the parent session.', choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
        ),
        migrations.AlterField(
            model_name='award',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='awards', to='api.Organization', help_text=b'\n            The organization that will confer the award.  Note that this may be different than the organization running the parent session.'),
        ),
        migrations.AlterField(
            model_name='award',
            name='rounds',
            field=models.IntegerField(help_text=b'\n            The number of rounds that will be used in determining the award.  Note that this may be fewer than the total number of rounds (rounds) in the parent session.', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='picture',
            field=models.ImageField(help_text=b'\n            The on-stage session picture (as opposed to the "official" photo).', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final placement/rank of the contestant for the entire session (ie, not a specific award).', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='judge',
            name='person',
            field=models.ForeignKey(related_name='sessions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='convention',
            field=models.ForeignKey(related_name='sessions', to='api.Convention'),
        ),
        migrations.AlterField(
            model_name='session',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of session.  Generally this will be either quartet or chorus, with the exception being International and Midwinter which hold exclusive Collegiate and Senior sessions respectively.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='num_rounds',
            field=models.IntegerField(default=1, help_text=b'\n            Number of rounds (rounds) for the session.', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='session',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='sessions', editable=False, to='api.Organization', help_text=b'\n            The organization that will confer the award.  Note that this may be different than the organization running the parent session.'),
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('level', 'kind', 'year', 'goal', 'organization', 'session')]),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('group', 'session')]),
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('session', 'kind', 'category', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='round',
            unique_together=set([('session', 'kind')]),
        ),
    ]
