# Generated by Django 4.2.4 on 2023-09-25 04:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libraryapp', '0019_bookcart_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryPdf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.pdfbook')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
