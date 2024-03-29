# Generated by Django 3.2.4 on 2021-06-19 11:39

from django.db import migrations
import ia_storage.fields
import ia_storage.storage


class Migration(migrations.Migration):

    dependencies = [
        ("calaccess_processed", "0015_auto_20180416_2200"),
    ]

    operations = [
        migrations.AlterField(
            model_name="processeddatafile",
            name="file_archive",
            field=ia_storage.fields.InternetArchiveFileField(
                blank=True,
                help_text="An archive of the processed file",
                max_length=255,
                storage=ia_storage.storage.InternetArchiveStorage,
                upload_to="",
                verbose_name="archive of processed file",
            ),
        ),
        migrations.AlterField(
            model_name="processeddatazip",
            name="zip_archive",
            field=ia_storage.fields.InternetArchiveFileField(
                help_text="An archived zip of processed files",
                max_length=255,
                storage=ia_storage.storage.InternetArchiveStorage,
                upload_to="",
                verbose_name="zip archive",
            ),
        ),
    ]
