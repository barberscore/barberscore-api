# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_rename_panel_contest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('contest', 'group')},
        ),
        migrations.AlterModelOptions(
            name='judge',
            options={'ordering': ('contest', 'kind', 'slot')},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ('contest', 'kind')},
        ),
        migrations.RenameField(
            model_name='award',
            old_name='panel',
            new_name='contest',
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='panel',
            new_name='contest',
        ),
        migrations.RenameField(
            model_name='judge',
            old_name='panel',
            new_name='contest',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='panel',
            new_name='contest',
        ),
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', to='api.Convention'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The Contest is different than the award objective.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='size',
            field=models.IntegerField(help_text=b'\n            Size of the judging contest (typically three or five.)', choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='judge',
            name='person',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('group', 'contest')]),
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('contest', 'kind', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('contest', 'kind')]),
        ),
    ]
