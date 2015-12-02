# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0064_auto_20151025_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='district',
        ),
        migrations.RemoveField(
            model_name='judge',
            name='district',
        ),
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([('level', 'kind', 'year', 'goal', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='convention',
            unique_together=set([('organization', 'kind', 'year')]),
        ),
        migrations.RemoveField(
            model_name='contest',
            name='district',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='district',
        ),
        migrations.DeleteModel(
            name='District',
        ),
    ]
