# Generated by Django 2.2.27 on 2022-10-14 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bhs', '0014_auto_20220907_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='district_display_name',
            field=models.CharField(default='', help_text='\n            Used to override the display of the district name/abbr in case of multi-district conventions.', max_length=255),
        ),
    ]
