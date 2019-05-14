# Generated by Django 2.1.8 on 2019-05-10 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bhs', '0004_auto_20190506_1158'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='group',
            name='parent',
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='member',
            name='group',
        ),
        migrations.RemoveField(
            model_name='member',
            name='person',
        ),
        migrations.AlterUniqueTogether(
            name='officer',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='officer',
            name='group',
        ),
        migrations.RemoveField(
            model_name='officer',
            name='person',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='Officer',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]