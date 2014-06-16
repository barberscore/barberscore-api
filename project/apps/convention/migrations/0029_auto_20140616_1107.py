# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0028_auto_20140616_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='twitter',
            field=models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the contestant.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')]),
        ),
    ]
