# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_rename_contest_award'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competitor',
            options={'ordering': ('award', 'contestant')},
        ),
        migrations.RenameField(
            model_name='competitor',
            old_name='contest',
            new_name='award',
        ),
        migrations.AlterField(
            model_name='award',
            name='goal',
            field=models.IntegerField(help_text=b'\n            The objective of the award', choices=[(1, b'Championship'), (2, b'Qualifier')]),
        ),
        migrations.AlterField(
            model_name='award',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='awards', to='api.Organization'),
        ),
        migrations.AlterField(
            model_name='award',
            name='panel',
            field=models.ForeignKey(related_name='awards', to='api.Panel'),
        ),
        migrations.AlterField(
            model_name='panel',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The Panel is different than the award objective.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
        ),
        migrations.AlterUniqueTogether(
            name='competitor',
            unique_together=set([('contestant', 'award')]),
        ),
    ]
