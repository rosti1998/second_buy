# Generated by Django 4.2.3 on 2023-07-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_alter_item_item_photo_inquiry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inquiry',
            name='profile',
        ),
        migrations.AddField(
            model_name='inquiry',
            name='email_address',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
