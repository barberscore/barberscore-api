# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.uuid
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20150126_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True), blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True), blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True), blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True), blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singer',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True), blank=True),
            preserve_default=True,
        ),
    ]
