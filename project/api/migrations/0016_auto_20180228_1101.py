# Generated by Django 2.0.2 on 2018-02-28 19:01

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20180228_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (2, 'Built'), (5, 'Invited'), (7, 'Withdrawn'), (10, 'Submitted'), (20, 'Approved'), (52, 'Scratched'), (55, 'Disqualified')], default=0, help_text='DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.'),
        ),
    ]