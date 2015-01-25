# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.uuid
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150124_2108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('year', models.IntegerField(default=2015, max_length=4, choices=[(1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)])),
                ('level', models.IntegerField(default=1, choices=[(1, b'International'), (2, b'District')])),
                ('dates', models.CharField(max_length=200, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('district', models.ForeignKey(blank=True, to='api.District', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='quartetmembership',
            name='from_date',
        ),
        migrations.RemoveField(
            model_name='quartetmembership',
            name='to_date',
        ),
    ]
