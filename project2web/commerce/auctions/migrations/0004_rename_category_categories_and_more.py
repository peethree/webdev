# Generated by Django 4.2 on 2023-05-11 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_category_auction_categories'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Categories',
        ),
        migrations.RenameField(
            model_name='auction',
            old_name='categories',
            new_name='category',
        ),
    ]
