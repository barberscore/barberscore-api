# Generated by Django 2.0.8 on 2018-08-21 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mc_pk',
            field=models.CharField(blank=True, db_index=True, max_length=36, null=True, unique=True),
        ),
    ]
