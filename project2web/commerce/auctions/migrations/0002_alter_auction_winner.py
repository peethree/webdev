# Generated by Django 4.2 on 2023-05-09 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='winner',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
