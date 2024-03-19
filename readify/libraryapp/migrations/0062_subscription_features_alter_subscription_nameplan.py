# Generated by Django 4.2.5 on 2024-02-13 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0061_subscription_nameplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='features',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='nameplan',
            field=models.CharField(choices=[('Gold', 'GOLD'), ('premium', 'PREMIUM')], max_length=255),
        ),
    ]