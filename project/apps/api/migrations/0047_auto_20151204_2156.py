# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_auto_20151204_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competitor',
            name='men',
        ),
        migrations.AlterField(
            model_name='competitor',
            name='name',
            field=models.CharField(unique=True, max_length=255, editable=False),
        ),
        migrations.AlterField(
            model_name='competitor',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final ranking relative to this award.', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final placement/rank of the contestant for the entire contest (ie, not a specific award).', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final ranking relative to this session.', null=True, editable=False, blank=True),
        ),
    ]
