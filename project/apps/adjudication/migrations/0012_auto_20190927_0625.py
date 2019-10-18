# Generated by Django 2.2.5 on 2019-09-27 13:25

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('adjudication', '0011_auto_20190925_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (10, 'Built'), (20, 'Started'), (25, 'Completed'), (27, 'Finalized'), (30, 'Published')], default=0, help_text='DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.'),
        ),
    ]