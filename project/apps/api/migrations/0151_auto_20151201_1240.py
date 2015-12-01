# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0150_auto_20151201_1151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-convention__year', 'place')},
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='contest',
        ),
    ]
