# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.api.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20151013_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='end',
            field=models.DateField(help_text=b'\n            The retirement/deceased date of the resource.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='kind',
            field=models.IntegerField(default=0, help_text=b'\n            The kind of District.  Choices are BHS (International), District, and Affiliate.', choices=[(0, b'BHS'), (1, b'District'), (2, b'Affiliate')]),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200, unique=True, error_messages={b'unique': b'The name must be unique.  Add middle initials, suffixes, years, or other identifiers to make the name unique.'}, validators=[apps.api.validators.validate_trimmed]),
        ),
        migrations.AlterField(
            model_name='group',
            name='chapter_code',
            field=models.CharField(help_text=b'\n            The chapter code (only for choruses).', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='chapter_name',
            field=models.CharField(help_text=b'\n            The chapter name (only for choruses).', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='end',
            field=models.DateField(help_text=b'\n            The retirement/deceased date of the resource.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='kind',
            field=models.IntegerField(default=1, help_text=b'\n            The kind of group; choices are Quartet or Chorus.', choices=[(1, b'Quartet'), (2, b'Chorus')]),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200, unique=True, error_messages={b'unique': b'The name must be unique.  Add middle initials, suffixes, years, or other identifiers to make the name unique.'}, validators=[apps.api.validators.validate_trimmed]),
        ),
        migrations.AlterField(
            model_name='person',
            name='end',
            field=models.DateField(help_text=b'\n            The retirement/deceased date of the resource.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='kind',
            field=models.IntegerField(default=1, help_text=b'\n            Most persons are individuals; however, they can be grouped into teams for the purpose of multi-arranger songs.', choices=[(1, b'Individual'), (2, b'Team')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200, unique=True, error_messages={b'unique': b'The name must be unique.  Add middle initials, suffixes, years, or other identifiers to make the name unique.'}, validators=[apps.api.validators.validate_trimmed]),
        ),
    ]
