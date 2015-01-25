# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_quartetmembership_contest'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuartetPerformance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round', models.IntegerField(blank=True, null=True, choices=[(1, b'Finals'), (2, b'Semi-Finals'), (3, b'Quarter-Finals')])),
                ('contest', models.ForeignKey(to='api.Contest')),
                ('quartet', models.ForeignKey(to='api.Quartet')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
