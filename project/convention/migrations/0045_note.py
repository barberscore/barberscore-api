# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0044_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile', models.ForeignKey(to='convention.Profile', to_field='id')),
                ('contestant', models.ForeignKey(to='convention.Contestant', to_field='id')),
                ('note', models.TextField(help_text=b'\n            Notes on each contestant.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
