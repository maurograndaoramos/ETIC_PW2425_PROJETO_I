# Generated by Django 5.0.6 on 2024-06-19 00:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("drive", "0006_file_drive_file_hash_6fb242_idx"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="folder",
            name="hash",
            field=models.CharField(
                default=1, editable=False, max_length=64, unique=True
            ),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name="folder",
            index=models.Index(fields=["hash"], name="drive_folde_hash_edd730_idx"),
        ),
    ]
