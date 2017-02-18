# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 23:54
from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    PerformancePrivate = apps.get_model("app", "PerformancePrivate")
    PerformanceScore = apps.get_model("app", "PerformanceScore")
    cs = PerformanceScore.objects.all()
    for c in cs:
        t = c.performance_ptr
        n = PerformancePrivate(
            performance=t,
            rank=c.rank,
            mus_points=c.mus_points,
            prs_points=c.prs_points,
            sng_points=c.sng_points,
            total_points=c.total_points,
            mus_score=c.mus_score,
            prs_score=c.prs_score,
            sng_score=c.sng_score,
            total_score=c.total_score,
        )
        n.save()


def reverse(apps, schema_editor):
    PerformancePrivate = apps.get_model("app", "PerformancePrivate")
    cp = PerformancePrivate.objects.all()
    cp.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_performanceprivate'),
    ]

    operations = [
        migrations.RunPython(forward, reverse)
    ]
