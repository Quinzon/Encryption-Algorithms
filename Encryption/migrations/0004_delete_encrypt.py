# Generated by Django 4.1 on 2023-02-28 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Encryption", "0003_alter_encrypt_file"),
    ]

    operations = [
        migrations.DeleteModel(
            name="EnCrypt",
        ),
    ]
