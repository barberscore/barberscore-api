# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0031_auto_20140617_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='startdate',
            field=models.DateField(help_text=b'\n            The start date of the contest.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='name',
            field=models.CharField(help_text=b'\n            The verbose name of the contest.', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='contest_level',
            field=models.IntegerField(default=1, help_text=b'\n            The contest level:  International, District, etc..', choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contest',
            name='contest_type',
            field=models.IntegerField(default=1, help_text=b'\n            The contest type:  Quartet, Chorus, Collegiate or Senior.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Collegiate'), (4, b'Senior')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='stagetime',
            field=models.DateTimeField(default=b'2014-01-01 00:00Z', help_text=b'\n            The approximate stagetime of the performance, in\n            the local time of the venue.'),
        ),
    ]
