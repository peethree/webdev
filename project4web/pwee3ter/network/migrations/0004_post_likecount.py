# Generated by Django 4.2 on 2023-06-25 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_remove_post_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likecount',
            field=models.IntegerField(default=0),
        ),
    ]