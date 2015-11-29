# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0137_auto_20151129_0617'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['contest', 'kind']},
        ),
        migrations.AlterField(
            model_name='day',
            name='contest',
            field=models.ForeignKey(related_name='days', to='api.Contest'),
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('contest', 'kind')]),
        ),
    ]
