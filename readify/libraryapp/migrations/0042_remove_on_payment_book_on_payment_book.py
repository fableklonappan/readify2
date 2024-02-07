# Generated by Django 4.2.5 on 2023-10-05 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0041_remove_paymenthistory_book_paymenthistory_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='on_payment',
            name='book',
        ),
        migrations.AddField(
            model_name='on_payment',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.addbook'),
        ),
    ]