# Generated by Django 4.2.5 on 2023-10-03 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0028_bookcart_cartstock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]