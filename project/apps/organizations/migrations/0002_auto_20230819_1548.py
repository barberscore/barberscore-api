# Generated by Django 2.2.27 on 2023-08-19 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='division',
            old_name='parent_district',
            new_name='district',
        ),
        migrations.AlterField(
            model_name='organization',
            name='drcj_nomen',
            field=models.CharField(default='DRCJ', help_text='String that should be used to replace "DRCJ" references on reports.', max_length=255, verbose_name='DRCJ nomen'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(default='', help_text='\n            e.g. Barbershop Harmony Society', max_length=255),
        ),
    ]
