# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20150125_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quartet',
            name='old_id',
        ),
        migrations.RemoveField(
            model_name='singer',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='singer',
            name='old_id',
        ),
        migrations.AddField(
            model_name='chapter',
            name='blurb',
            field=models.TextField(help_text=b'\n            A description/bio describing the resource.  Max 1000 characters.', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='email',
            field=models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='facebook',
            field=models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='location',
            field=models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='notes',
            field=models.TextField(help_text=b'\n            Notes (for internal use only).', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='twitter',
            field=models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='website',
            field=models.URLField(help_text=b'\n            The website URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorus',
            name='notes',
            field=models.TextField(help_text=b'\n            Notes (for internal use only).', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='district',
            name='blurb',
            field=models.TextField(help_text=b'\n            A description/bio describing the resource.  Max 1000 characters.', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='district',
            name='notes',
            field=models.TextField(help_text=b'\n            Notes (for internal use only).', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='district',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartet',
            name='notes',
            field=models.TextField(help_text=b'\n            Notes (for internal use only).', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='singer',
            name='blurb',
            field=models.TextField(help_text=b'\n            A description/bio describing the resource.  Max 1000 characters.', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='singer',
            name='facebook',
            field=models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='singer',
            name='location',
            field=models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='singer',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='singer',
            name='twitter',
            field=models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='singer',
            name='website',
            field=models.URLField(help_text=b'\n            The website URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chapter',
            name='district',
            field=models.ForeignKey(blank=True, to='api.District', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='blurb',
            field=models.TextField(help_text=b'\n            A description/bio describing the resource.  Max 1000 characters.', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='email',
            field=models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='facebook',
            field=models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='location',
            field=models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='twitter',
            field=models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='website',
            field=models.URLField(help_text=b'\n            The website URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='email',
            field=models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='facebook',
            field=models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='location',
            field=models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='twitter',
            field=models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='website',
            field=models.URLField(help_text=b'\n            The website URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='blurb',
            field=models.TextField(help_text=b'\n            A description/bio describing the resource.  Max 1000 characters.', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='email',
            field=models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='facebook',
            field=models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='location',
            field=models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='twitter',
            field=models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='website',
            field=models.URLField(help_text=b'\n            The website URL of the resource.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singer',
            name='email',
            field=models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singer',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singer',
            name='notes',
            field=models.TextField(help_text=b'\n            Notes (for internal use only).', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True),
            preserve_default=True,
        ),
    ]
