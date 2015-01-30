# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_auto_20150129_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='convention',
            options={'ordering': ['district', 'kind', 'year']},
        ),
        migrations.AlterModelOptions(
            name='quartet',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='singer',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='convention',
            name='level',
        ),
        migrations.RemoveField(
            model_name='singer',
            name='timezone',
        ),
        migrations.AddField(
            model_name='convention',
            name='district',
            field=models.ForeignKey(blank=True, to='api.District', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convention',
            name='slug',
            field=autoslug.fields.AutoSlugField(null=True, editable=False, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='kind',
            field=models.IntegerField(default=1, choices=[(0, b'BHS'), (1, b'District'), (2, b'Affiliate')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='district',
            field=models.ForeignKey(blank=True, to='api.District', help_text=b'\n            This is the district the quartet is officially representing in the contest.', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singer',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
    ]
