# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20150508_0627'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='year',
            field=models.IntegerField(default=2015, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'International'), (2, b'District'), (3, b'Regional')]),
        ),
    ]
