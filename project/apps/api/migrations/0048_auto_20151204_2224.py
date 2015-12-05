# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import django.utils.timezone
import model_utils.fields
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20151204_2156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='award',
            options={'ordering': ('-year', 'organization', 'level', 'kind', 'goal')},
        ),
        migrations.AddField(
            model_name='contest',
            name='history',
            field=models.IntegerField(default=0, help_text=b'Used to manage state for historical imports.', choices=[(0, b'New'), (10, b'None'), (20, b'PDF'), (30, b'Places'), (40, b'Incomplete'), (50, b'Complete')]),
        ),
        migrations.AddField(
            model_name='contest',
            name='history_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'History last updated', monitor=b'history'),
        ),
        migrations.AddField(
            model_name='contest',
            name='scoresheet_csv',
            field=models.FileField(help_text=b'\n            The parsed scoresheet (used for legacy imports).', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='scoresheet_pdf',
            field=models.FileField(help_text=b'\n            The historical PDF OSS.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='award',
            name='goal',
            field=models.IntegerField(help_text=b'\n            The objective of the award.', choices=[(1, b'Championship'), (2, b'Qualifier')]),
        ),
        migrations.AlterField(
            model_name='award',
            name='history',
            field=models.IntegerField(default=0, help_text=b'Used to manage state for historical imports.', choices=[(0, b'New'), (10, b'None'), (20, b'PDF'), (30, b'Places'), (40, b'Incomplete'), (50, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of the award.  Note that this may be different than the kind of the parent contest.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (5, b'Novice')]),
        ),
        migrations.AlterField(
            model_name='award',
            name='level',
            field=models.IntegerField(help_text=b'\n            The level of the award.  Note that this may be different than the level of the parent contest.', choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
        ),
        migrations.AlterField(
            model_name='award',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='awards', to='api.Organization', help_text=b'\n            The organization that will confer the award.  Note that this may be different than the organization running the parent contest.'),
        ),
        migrations.AlterField(
            model_name='award',
            name='qual_score',
            field=models.FloatField(help_text=b'\n            The objective of the award.  Note that if the goal is `qualifier` then this must be set.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='award',
            name='rounds',
            field=models.IntegerField(help_text=b'\n            The number of rounds that will be used in determining the award.  Note that this may be fewer than the total number of rounds (sessions) in the parent contest.', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
    ]
