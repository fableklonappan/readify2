# Generated by Django 4.2.5 on 2024-01-30 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0051_remove_rentalrequest_borrow_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalrequest',
            name='total',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
