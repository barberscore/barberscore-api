# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_convention_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ('level', 'kind', 'year', 'district')},
        ),
        migrations.AlterField(
            model_name='convention',
            name='district',
            field=models.ForeignKey(blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Summer'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pan-Pacific')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='year',
            field=models.IntegerField(default=2015, null=True, blank=True, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
    ]
