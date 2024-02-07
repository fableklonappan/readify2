# Generated by Django 4.2.5 on 2023-10-05 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0037_remove_paymenthistory_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
