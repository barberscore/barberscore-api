# Generated by Django 2.2.5 on 2019-09-25 20:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adjudication', '0010_outcome_is_single'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='penalties',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(30, 'Repeating Substantial Portions of a Song'), (32, 'Instrumental Accompaniment'), (34, 'Chorus Exceeding 4-Part Texture'), (36, 'Excessive Melody Not in Inner Part'), (38, 'Lack of Characteristic Chord Progression'), (39, 'Excessive Lyrics < 4 parts'), (40, 'Primarily Patriotic/Religious Intent'), (50, 'Sound Equipment or Electronic Enhancement')]), blank=True, default=list, size=None),
        ),
    ]
