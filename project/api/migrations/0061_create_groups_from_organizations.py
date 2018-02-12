# Generated by Django 2.0.2 on 2018-02-11 02:45

from django.db import migrations


def create_groups_from_organizations(apps, schema_editor):
    Group = apps.get_model('api', 'Group')
    Organization = apps.get_model('api', 'Organization')
    organizations = Organization.objects.filter(
        kind__lte=30,
    )
    for organization in organizations:
        group, created = Group.objects.get_or_create(
            name=organization.name,
            status=organization.status,
            kind=organization.kind,
            code=organization.code,
            start_date=organization.start_date,
            end_date=organization.end_date,
            location=organization.location,
            website=organization.website,
            facebook=organization.facebook,
            twitter=organization.twitter,
            email=organization.email,
            phone=organization.phone,
            description=organization.description,
            notes=organization.notes,
            mem_status=organization.mem_status,
            organization=organization,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0060_auto_20180210_1912'),
    ]

    operations = [
        migrations.RunPython(create_groups_from_organizations),
    ]