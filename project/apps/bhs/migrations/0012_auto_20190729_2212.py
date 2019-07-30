# Generated by Django 2.2.3 on 2019-07-30 05:12

from django.db import migrations


class Migration(migrations.Migration):
    def forward(apps, schema_editor):
        Group = apps.get_model('bhs.group')
        gs = Group.objects.filter(
            kind__in=[
                41,
                32,
            ]
        ).exclude(parent__isnull=True)
        for g in gs:
            if g.kind == 41:
                g.district = g.parent.district
            elif g.kind == 32:
                g.district = g.parent.parent.district
                g.chapters = g.parent.name
            g.save()


    dependencies = [
        ('bhs', '0011_auto_20190729_2207'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]