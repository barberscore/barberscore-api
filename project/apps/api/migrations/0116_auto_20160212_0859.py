# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0115_contestant_award'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='contest',
            name='award',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='session',
        ),
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('award', 'place')},
        ),
        migrations.AlterField(
            model_name='convention',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='conventions', to='api.Organization', help_text=b'\n            The organization hosting the convention.'),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('performer', 'award')]),
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='contest',
        ),
        migrations.DeleteModel(
            name='Contest',
        ),
    ]
