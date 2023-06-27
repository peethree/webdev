# Generated by Django 4.2 on 2023-06-26 11:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_post_likecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='disliked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]