# Generated by Django 4.2.5 on 2024-03-04 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0081_alter_walletdata_total_copywalletdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copywalletdata',
            name='purchase_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
