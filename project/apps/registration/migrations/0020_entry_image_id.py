# Generated by Django 2.2.5 on 2019-09-25 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0019_session_registration_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='image_id',
            field=models.CharField(blank=True, default='missing_image', help_text='The cloudinary image reference.', max_length=255),
        ),
    ]
