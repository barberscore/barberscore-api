# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20151216_2049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judge',
            options={'ordering': ('round', 'kind', 'category', 'slot')},
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('round', 'kind', 'category', 'slot')]),
        ),
    ]
