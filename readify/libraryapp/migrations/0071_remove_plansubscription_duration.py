# Generated by Django 4.2.5 on 2024-02-13 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0070_plansubscription_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plansubscription',
            name='duration',
        ),
    ]
