# Generated by Django 4.2.3 on 2023-07-24 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_remove_inquiry_profile_inquiry_email_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]