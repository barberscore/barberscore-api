# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0096_remove_person_nick_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('contest', 'category', 'slot'), ('contest', 'person')]),
        ),
    ]
