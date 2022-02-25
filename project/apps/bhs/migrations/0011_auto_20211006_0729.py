# Generated by Django 2.2.20 on 2021-10-06 14:29

import apps.bhs.fields
import cloudinary_storage.storage
from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('bhs', '0010_auto_20210929_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='bbstix_practice_report',
            field=models.FileField(blank=True, default='', help_text='This BBSTIX report include practice judge data.', storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=apps.bhs.fields.UploadPath('bbstix_practice_report'), verbose_name='BBSTIX Report (with Practice Judges)'),
        ),
        migrations.AlterField(
            model_name='convention',
            name='bbstix_report',
            field=models.FileField(blank=True, default='', storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=apps.bhs.fields.UploadPath('bbstix_report'), verbose_name='BBSTIX Report'),
        ),
        migrations.AlterField(
            model_name='convention',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(-10, 'Inactive'), (-5, 'Cancelled'), (0, 'New'), (5, 'Built'), (10, 'Active')], default=0, help_text='DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.'),
        ),
    ]