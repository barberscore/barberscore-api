# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0095_person_nick_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='nick_name',
        ),
    ]
