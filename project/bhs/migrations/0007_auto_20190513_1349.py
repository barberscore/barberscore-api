# Generated by Django 2.1.8 on 2019-05-13 20:49

from django.db import migrations

def forward(apps, schema_editor):
    Old = apps.get_model('api.person')
    New = apps.get_model('bhs.person')

    items = Old.objects.values()
    for item in items:
        New.objects.create(**item)

    Old = apps.get_model('api.group')
    New = apps.get_model('bhs.group')

    items = Old.objects.values()
    for item in items:
        New.objects.create(**item)

    Old = apps.get_model('api.member')
    New = apps.get_model('bhs.member')

    items = Old.objects.values()
    for item in items:
        New.objects.create(**item)

    Old = apps.get_model('api.officer')
    New = apps.get_model('bhs.officer')

    items = Old.objects.values(
        'id',
        'status',
        'start_date',
        'end_date',
        'mc_pk',
        'person_id',
        'group_id',
        'office__code',
    )
    for item in items:
        item['office'] = item.pop('office__code')
    for item in items:
        New.objects.create(**item)

    Old = apps.get_model('api.chart')
    New = apps.get_model('bhs.chart')

    items = Old.objects.values()
    for item in items:
        New.objects.create(**item)

    Old = apps.get_model('api.repertory')
    New = apps.get_model('bhs.repertory')

    items = Old.objects.values()
    for item in items:
        New.objects.create(**item)

    # StateLog = apps.get_model('django_fsm_log.statelog')

    # logs = StateLog.objects.filter(
    #     content_type_id=31
    # )
    # logs.update(content_type_id=36)

    # logs = StateLog.objects.filter(
    #     content_type_id=19
    # )
    # logs.update(content_type_id=35)

    # logs = StateLog.objects.filter(
    #     content_type_id=16
    # )
    # logs.update(content_type_id=60)

    # logs = StateLog.objects.filter(
    #     content_type_id=18
    # )
    # logs.update(content_type_id=61)



class Migration(migrations.Migration):

    dependencies = [
        ('bhs', '0006_auto_20190513_1341'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]