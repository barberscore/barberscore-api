# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0007_delete_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contest', models.ForeignKey(to='bbs.Contest', to_field='id')),
                ('contestant', models.ForeignKey(to='bbs.Contestant', to_field='id')),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('song1', models.CharField(max_length=200)),
                ('mus1', models.IntegerField()),
                ('prs1', models.IntegerField()),
                ('sng1', models.IntegerField()),
                ('song2', models.CharField(max_length=200)),
                ('mus2', models.IntegerField()),
                ('prs2', models.IntegerField()),
                ('sng2', models.IntegerField()),
                ('men_on_stage', models.IntegerField(default=4, null=True)),
            ],
            options={
                'ordering': [b'contestant'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contest',
            name='performers',
            field=models.ManyToManyField(to='bbs.Contestant', through='bbs.Performance'),
            preserve_default=True,
        ),
    ]
