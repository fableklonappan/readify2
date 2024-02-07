# Generated by Django 4.2.5 on 2023-10-05 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0043_remove_paymenthistory_book_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymenthistory',
            name='bookpayment',
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.addbook'),
        ),
    ]