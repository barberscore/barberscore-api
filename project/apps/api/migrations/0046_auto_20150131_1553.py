# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20150131_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChorusAward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('award', models.ForeignKey(to='api.Award')),
                ('chorus', models.ForeignKey(to='api.Chorus')),
                ('contest', models.ForeignKey(to='api.Contest')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chorus',
            name='awards',
            field=models.ManyToManyField(related_name='choruses', through='api.ChorusAward', to='api.Award'),
            preserve_default=True,
        ),
    ]
