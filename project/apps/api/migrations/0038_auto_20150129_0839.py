# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20150128_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='contest',
            name='dates',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='location',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='timezone',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='baritone',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='bass',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='tenor',
        ),
        migrations.AddField(
            model_name='quartet',
            name='district',
            field=models.ForeignKey(blank=True, to='api.District', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'Summer'), (2, b'Midwinter')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singer',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
