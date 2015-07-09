# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0143_auto_20150708_0507'),
    ]

    operations = [
        migrations.AlterField('person', 'slug', models.CharField(max_length=255)),
        migrations.AlterField('group', 'slug', models.CharField(max_length=255)),
        migrations.AlterField('district', 'slug', models.CharField(max_length=255)),
        migrations.AlterField('convention', 'slug', models.CharField(max_length=255)),
        migrations.AlterField('contest', 'slug', models.CharField(max_length=255)),
        migrations.AlterField('contestant', 'slug', models.CharField(max_length=255)),
        migrations.AlterField('singer', 'slug', models.CharField(max_length=255)),
        migrations.AlterField('director', 'slug', models.CharField(max_length=255)),
        migrations.AlterField('song', 'slug', models.CharField(max_length=255)),
        migrations.AlterField('performance', 'slug', models.CharField(max_length=255)),
    ]
