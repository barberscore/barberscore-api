# Generated by Django 2.1.1 on 2018-10-01 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0122_merge_20181001_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='level',
            field=models.IntegerField(choices=[(10, 'Championship'), (30, 'Qualifier'), (45, 'Representative'), (50, 'Deferred'), (60, 'Manual')]),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='legacy_name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
