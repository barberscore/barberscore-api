# Generated by Django 2.2.27 on 2022-09-08 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adjudication', '0027_auto_20220822_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='outcome',
            name='print_on_finals_oss',
            field=models.BooleanField(default=False, help_text='\n            Show this outcome on the Finals OSS.'),
        ),
    ]
