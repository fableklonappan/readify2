# Generated by Django 4.2.5 on 2024-02-27 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0078_merge_0074_walletdata_0077_remove_walletdata_duration'),
    ]

    operations = [
        migrations.DeleteModel(
            name='walletdata',
        ),
    ]