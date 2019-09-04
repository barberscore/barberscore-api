# Generated by Django 2.2.4 on 2019-09-04 13:15

from django.db import migrations

def forward(apps, schema_editor):
    Entry = apps.get_model('registration.entry')
    Group = apps.get_model('bhs.group')
    Chart = apps.get_model('bhs.chart')

    es = Entry.objects.all()
    for e in es:
        try:
            g = Group.objects.get(id=e.group_id)
        except Group.DoesNotExist:
            raise RuntimeError(e)
        e.representing = g.get_district_display()
        if not e.representing:
            raise RuntimeError(e)
        g.participants = e.participants
        g.chapters = e.chapters
        g.pos = e.pos
        rs = e.repertories.all()
        for r in rs:
            try:
                c = Chart.objects.get(id=r.chart_id)
            except Chart.DoesNotExist:
                raise RuntimeError(e, r.chart_id)
            g.charts.add(c)
        e.save()
        g.save()

class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20190903_1319'),
    ]

    operations = [
        migrations.RunPython(forward),
    ]
