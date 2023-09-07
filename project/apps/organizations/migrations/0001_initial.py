# Generated by Django 2.2.27 on 2023-08-19 22:04

import apps.organizations.fields
import cloudinary_storage.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Organization', help_text='\n            e.g. Far Western District', max_length=255)),
                ('abbreviation', models.CharField(help_text='\n            e.g. FWD', max_length=255)),
                ('logo', models.FileField(blank=True, default='', help_text='Logo should be xx x xx in JPG format.', storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=apps.organizations.fields.UploadPath('district_logos'))),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Organization', help_text='\n            e.g. Barbershop Harmony Society', max_length=255)),
                ('abbreviation', models.CharField(help_text='\n            e.g. BHS', max_length=255)),
                ('logo', models.FileField(blank=True, default='', help_text='Logo should be xx x xx in JPG format.', storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=apps.organizations.fields.UploadPath('organization_logos'))),
                ('district_nomen', models.CharField(default='District', help_text='String that should be used to replace "District" references on reports.', max_length=255)),
                ('division_nomen', models.CharField(default='Division', help_text='String that should be used to replace "Division" references on reports.', max_length=255)),
                ('drcj_nomen', models.CharField(default='DRCJ', help_text='String that should be used to replace "DRCJ" references on reports.', max_length=255)),
                ('default_owners', models.ManyToManyField(related_name='organizations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Organization', help_text='\n            e.g. FWD Northwest', max_length=255)),
                ('abbreviation', models.CharField(help_text='\n            e.g. fwdnw', max_length=255)),
                ('logo', models.FileField(blank=True, default='', help_text='Logo should be xx x xx in JPG format.', storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=apps.organizations.fields.UploadPath('division_logos'))),
                ('parent_district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district', to='organizations.District')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='district',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='organizations.Organization'),
        ),
    ]