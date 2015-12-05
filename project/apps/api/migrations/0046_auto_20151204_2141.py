# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20151204_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='convention',
        ),
        migrations.AlterField(
            model_name='contestant',
            name='men',
            field=models.IntegerField(default=4, help_text=b'\n            The number of men on stage.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='name',
            field=models.CharField(unique=True, max_length=255, editable=False),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='picture',
            field=models.ImageField(help_text=b'\n            The on-stage contest picture (as opposed to the "official" photo).', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final placement/rank of the contestant for the entire contest (ie, not a specific award).', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='prelim',
            field=models.FloatField(help_text=b'\n            The incoming prelim score.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='seed',
            field=models.IntegerField(help_text=b'\n            The incoming rank based on prelim score.', null=True, blank=True),
        ),
    ]
