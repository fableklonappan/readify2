# Generated by Django 4.2.5 on 2023-10-05 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0046_on_payment_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='on_payment',
            name='book',
        ),
    ]