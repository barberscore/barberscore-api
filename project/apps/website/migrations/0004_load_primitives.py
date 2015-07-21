from __future__ import unicode_literals

from django.db import migrations


def load_primitives(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Primitive = apps.get_model("website", "Primitive")
    Primitive.objects.create(
        name='Group',
    )
    Primitive.objects.create(
        name='Person',
    )
    Primitive.objects.create(
        name='Song',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20150720_0955'),
    ]

    operations = [
        migrations.RunPython(load_primitives),
    ]
