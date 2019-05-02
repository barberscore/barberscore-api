# Generated by Django 2.1.8 on 2019-05-02 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0125_auto_20190501_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_expelled',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='person',
            name='is_honorary',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='person',
            name='is_suspended',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_deceased',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]