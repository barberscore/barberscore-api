# Generated by Django 2.2.3 on 2019-07-13 19:41

from django.db import migrations

def forward(apps, schema_editor):
    Entry = apps.get_model('smanager.entry')
    Group = apps.get_model('bhs.group')
    User = apps.get_model('rest_framework_jwt.user')

    es = Entry.objects.filter(
        group_id__isnull=False,
    )
    for e in es:
        group = Group.objects.get(id=e.group_id)
        fs = group.officers.filter(
            status__gt=0,
        )
        for f in fs:
            person = f.person
            if not person.email:
                continue
            try:
                user = User.objects.get(
                    email=person.email,
                )
            except User.DoesNotExist:
                continue
            e.owners.add(user)

class Migration(migrations.Migration):

    dependencies = [
        ('smanager', '0007_auto_20190713_1236'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
