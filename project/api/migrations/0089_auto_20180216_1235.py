# Generated by Django 2.0.2 on 2018-02-16 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0088_office_bhs_pk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='part',
            field=models.IntegerField(blank=True, choices=[(1, 'Tenor'), (2, 'Lead'), (3, 'Baritone'), (4, 'Bass')], null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='part',
            field=models.IntegerField(blank=True, choices=[(1, 'Tenor'), (2, 'Lead'), (3, 'Baritone'), (4, 'Bass')], null=True),
        ),
    ]
