# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0022_performance_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='session',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Collegiate Finals'), (2, b'Quartet Quarter-Finals Session #1'), (3, b'Quartet Quarter-Finals Session #2'), (4, b'Chorus Finals Session #1'), (5, b'Chorus Finals Session #2'), (6, b'Quartet Semi-Finals'), (7, b'Quartet Finals')]),
        ),
    ]
