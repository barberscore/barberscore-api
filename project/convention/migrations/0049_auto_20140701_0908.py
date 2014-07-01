# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_districts(apps, schema_editor):
    Contestant = apps.get_model("convention", "Contestant")
    contestants = Contestant.objects.all()

    UNK = 0
    CAR = 1
    CSD = 2
    DIX = 3
    EVG = 4
    FWD = 5
    ILL = 6
    JAD = 7
    LOL = 8
    MAD = 9
    NED = 10
    NSC = 11
    ONT = 12
    PIO = 13
    RMD = 14
    SLD = 15
    SUN = 16
    SWD = 17
    BABS = 18
    BHA = 19
    NZABS = 20
    SNOBS = 21

    DISTRICT_CHOICES = (
        (UNK, 'UNK'),
        (CAR, 'CAR'),
        (CSD, 'CSD'),
        (DIX, 'DIX'),
        (EVG, 'EVG'),
        (FWD, 'FWD'),
        (ILL, 'ILL'),
        (JAD, 'JAD'),
        (LOL, 'LOL'),
        (MAD, 'MAD'),
        (NED, 'NED'),
        (NSC, 'NSC'),
        (ONT, 'ONT'),
        (PIO, 'PIO'),
        (RMD, 'RMD'),
        (SLD, 'SLD'),
        (SUN, 'SUN'),
        (SWD, 'SWD'),
        (BABS, 'BABS'),
        (BHA, 'BHA'),
        (NZABS, 'NZABS'),
        (SNOBS, 'SNOBS'),
    )

    districts = DISTRICT_CHOICES

    for contestant in contestants:
        for district in districts:
            if contestant.district == district[1]:
                contestant.district_id = district[0]
                contestant.save()


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0048_auto_20140701_0908'),
    ]

    operations = [
        migrations.RunPython(update_districts),
    ]
