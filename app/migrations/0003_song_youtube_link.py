# Generated by Django 5.1.4 on 2025-01-27 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_mood_song_moods'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='youtube_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
