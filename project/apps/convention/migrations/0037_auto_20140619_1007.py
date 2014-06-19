# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0036_remove_contest_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='session',
            field=models.IntegerField(blank=True, help_text=b'\n            Contest rounds are broken down into sessions, which\n            are tracked here.', null=True, choices=[(1, b'Collegiate Finals, Tuesday July 1'), (2, b'Quartet Quarter-Finals Session #1, Wednesday July 2'), (3, b'Quartet Quarter-Finals Session #2, Wednesday July 2'), (4, b'Quartet Semi-Finals, Thursday July 3'), (5, b'Chorus Finals Session #1, Friday July 4'), (6, b'Chorus Finals Session #2, Friday July 4'), (7, b'Quartet Finals, Saturday July 5')]),
        ),
    ]
