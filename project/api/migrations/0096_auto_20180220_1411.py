# Generated by Django 2.0.2 on 2018-02-20 22:11

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0095_auto_20180220_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(-10, 'Inactive'), (-5, 'AIC'), (0, 'New'), (10, 'Active')], default=0, help_text='DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.'),
        ),
    ]
