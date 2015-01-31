# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0011_auto_20140521_0834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='performers',
            new_name='contestants',
        ),
    ]
