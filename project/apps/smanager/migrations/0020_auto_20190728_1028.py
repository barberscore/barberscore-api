# Generated by Django 2.2.3 on 2019-07-28 17:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smanager', '0019_auto_20190728_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='owners',
            field=models.ManyToManyField(related_name='conventions_old', to=settings.AUTH_USER_MODEL),
        ),
    ]
