# Generated by Django 2.2.27 on 2022-03-22 17:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adjudication', '0018_auto_20220318_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='penalties',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(30, 'Repeating Substantial Portions of a Song (V.A.2)'), (32, 'Instrumental Accompaniment (IX.A.2.a)'), (34, 'Chorus Exceeding 4-Part Texture (IX.A.2.b)'), (36, 'Excessive Melody Not in Inner Part (IX.A.2.c)'), (38, 'Lack of Characteristic Chord Progression (IX.A.2.d)'), (39, 'Excessive Lyrics < 4 parts (IX.A.2.e)'), (40, 'Primarily Patriotic/Religious Intent (IX.A.3)'), (44, 'Not in Good Taste (IX.A.3.b)'), (48, 'Non-members Performing on Stage (XI.A.1)'), (50, 'Sound Equipment or Electronic Enhancement (X.B.1-3)')]), blank=True, default=list, size=None),
        ),
    ]
