# Generated by Django 2.1.2 on 2018-10-09 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0135_auto_20181009_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='complete',
            name='group_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]