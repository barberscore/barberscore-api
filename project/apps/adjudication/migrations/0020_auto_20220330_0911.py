# Generated by Django 2.2.27 on 2022-03-30 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adjudication', '0019_auto_20220322_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='num',
            field=models.IntegerField(blank=True, help_text='The order of appearance for this round.', null=True),
        ),
    ]
