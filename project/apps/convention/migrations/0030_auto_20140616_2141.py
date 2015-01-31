# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0029_auto_20140616_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='stagetime',
            field=models.DateTimeField(help_text=b'\n            The approximate stagetime of the performance, in\n            the local time of the venue.'),
        ),
    ]
