# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20151206_2333'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competitor',
            options={'ordering': ('award', 'performer')},
        ),
        migrations.RenameField(
            model_name='competitor',
            old_name='contestant',
            new_name='performer',
        ),
        migrations.RenameField(
            model_name='director',
            old_name='contestant',
            new_name='performer',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='contestant',
            new_name='performer',
        ),
        migrations.RenameField(
            model_name='singer',
            old_name='contestant',
            new_name='performer',
        ),
        migrations.AlterField(
            model_name='performer',
            name='group',
            field=models.ForeignKey(related_name='performers', to='api.Group'),
        ),
        migrations.AlterField(
            model_name='performer',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='performers', blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='performer',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final placement/rank of the performer for the entire session (ie, not a specific award).', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performer',
            name='session',
            field=models.ForeignKey(related_name='performers', to='api.Session'),
        ),
        migrations.AlterUniqueTogether(
            name='competitor',
            unique_together=set([('performer', 'award')]),
        ),
        migrations.AlterUniqueTogether(
            name='director',
            unique_together=set([('performer', 'person')]),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('round', 'performer')]),
        ),
        migrations.AlterUniqueTogether(
            name='singer',
            unique_together=set([('performer', 'person')]),
        ),
    ]
