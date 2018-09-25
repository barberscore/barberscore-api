# Generated by Django 2.0.8 on 2018-09-16 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0113_competitor_contesting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='person',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='api.Person'),
        ),
    ]