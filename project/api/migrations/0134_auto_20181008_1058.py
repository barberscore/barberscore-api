# Generated by Django 2.1.2 on 2018-10-08 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0133_auto_20181008_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='selection',
            name='appearance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Appearance'),
        ),
        migrations.AddField(
            model_name='selection',
            name='convention',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Convention'),
        ),
        migrations.AddField(
            model_name='selection',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Round'),
        ),
        migrations.AddField(
            model_name='selection',
            name='score',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Score'),
        ),
        migrations.AddField(
            model_name='selection',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Session'),
        ),
        migrations.AddField(
            model_name='selection',
            name='song',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Song'),
        ),
    ]
