# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20150128_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuartetMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part', models.IntegerField(blank=True, null=True, choices=[(1, b'Lead'), (2, b'Tenor'), (3, b'Baritone'), (4, b'Bass')])),
                ('contest', models.ForeignKey(to='api.Contest')),
                ('quartet', models.ForeignKey(to='api.Quartet')),
                ('singer', models.ForeignKey(to='api.Singer')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='quartet',
            name='members',
            field=models.ManyToManyField(to='api.Singer', through='api.QuartetMember'),
            preserve_default=True,
        ),
    ]
