# Generated by Django 2.2.27 on 2022-04-11 17:01

import apps.adjudication.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adjudication', '0022_auto_20220407_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='code',
            field=models.CharField(blank=True, default='', help_text='\n            Short-form code.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='csa_report',
            field=models.FileField(blank=True, default='', upload_to=apps.adjudication.fields.UploadPath('csa_report'), verbose_name='CSA Report'),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='owners',
            field=models.ManyToManyField(blank=True, related_name='appearances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='pos',
            field=models.IntegerField(blank=True, help_text='Number of Singers on Stage', null=True, verbose_name='Participants on Stage'),
        ),
    ]
