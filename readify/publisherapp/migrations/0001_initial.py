# Generated by Django 3.2.16 on 2024-03-31 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('libraryapp', '0085_remove_rentalrequest_razorpay_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='viewcustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.paymenthistory')),
                ('rent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.rentalrequest')),
                ('subscriber', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.plansubscription')),
            ],
        ),
    ]
