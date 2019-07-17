# Generated by Django 2.2.3 on 2019-07-13 19:36

from django.db import migrations

def forward(apps, schema_editor):
    Session = apps.get_model('smanager.session')
    Person = apps.get_model('bhs.person')
    User = apps.get_model('rest_framework_jwt.user')

    ss = Session.objects.filter(
        convention__assignments__isnull=False,
    )
    for s in ss:
        assignments = s.convention.assignments.filter(
            category=5,
        ).distinct()
        for assignment in assignments:
            try:
                person = Person.objects.get(id=assignment.person_id)
            except Person.DoesNotExist:
                continue
            if not person.email:
                continue
            try:
                user = User.objects.get(
                    email=person.email,
                )
            except User.DoesNotExist:
                continue
            s.owners.add(user)


class Migration(migrations.Migration):

    dependencies = [
        ('smanager', '0006_auto_20190712_0907'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
