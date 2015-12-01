# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0147_panelist_convention'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='award',
            options={},
        ),
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('place',)},
        ),
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['kind']},
        ),
        migrations.AlterModelOptions(
            name='panelist',
            options={'ordering': ('convention', 'category', 'slot')},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['convention', 'kind']},
        ),
        migrations.AddField(
            model_name='award',
            name='year',
            field=models.IntegerField(default=2015, choices=[(2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945), (1944, 1944), (1943, 1943), (1942, 1942), (1941, 1941), (1940, 1940), (1939, 1939)]),
        ),
        migrations.AlterField(
            model_name='award',
            name='contest',
            field=models.ForeignKey(related_name='awards', on_delete=django.db.models.deletion.SET_NULL, to='api.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='contest',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, to='api.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='day',
            name='contest',
            field=models.ForeignKey(related_name='days', on_delete=django.db.models.deletion.SET_NULL, to='api.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='panel',
            name='contest',
            field=models.ForeignKey(related_name='panels', on_delete=django.db.models.deletion.SET_NULL, to='api.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='panelist',
            name='contest',
            field=models.ForeignKey(related_name='panelists', on_delete=django.db.models.deletion.SET_NULL, to='api.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='contest',
            field=models.ForeignKey(related_name='sessions', on_delete=django.db.models.deletion.SET_NULL, to='api.Contest', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('convention', 'kind')]),
        ),
        migrations.AlterUniqueTogether(
            name='panelist',
            unique_together=set([]),
        ),
    ]
