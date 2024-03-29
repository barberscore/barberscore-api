# Generated by Django 2.2.27 on 2023-08-20 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20230820_0530'),
        ('bhs', '0018_auto_20230819_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='organizations.Organization'),
        ),
        migrations.AddField(
            model_name='convention',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='org', to='organizations.Organization'),
        ),
        migrations.AddField(
            model_name='group',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='organizations.Organization'),
        ),
    ]
