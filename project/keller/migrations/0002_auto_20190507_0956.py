# Generated by Django 2.1.8 on 2019-05-07 16:56

from django.db import migrations

def forward(apps, schema_editor):
    OldSelection = apps.get_model('api.selection')
    NewSelection = apps.get_model('keller.selection')
    OldComplete = apps.get_model('api.complete')
    NewComplete = apps.get_model('keller.complete')
    OldFlat = apps.get_model('api.flat')
    NewFlat = apps.get_model('keller.flat')

    selections = OldSelection.objects.values()
    for selection in selections:
        NewSelection.objects.create(**selection)

    completes = OldComplete.objects.values()
    for complete in completes:
        NewComplete.objects.create(**complete)

    flats = OldFlat.objects.values()
    for flat in flats:
        NewFlat.objects.create(**flat)


class Migration(migrations.Migration):

    dependencies = [
        ('keller', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
