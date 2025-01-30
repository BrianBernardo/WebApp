from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Mood(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    moods = models.ManyToManyField(Mood, related_name="songs")
    youtube_embed_code = models.TextField(blank=True, null=True)  # Changed to TextField for embed code
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('song_detail', kwargs={'pk': self.pk})

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who created the playlist
    songs = models.ManyToManyField(Song)  # Songs added to the playlist

    def __str__(self):
        return self.name
class SongComment(models.Model):
    song = models.ForeignKey(Song, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  # This is the content field the form is referring to
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.song.title}"

    class Meta:
        ordering = ['created_at']

class Rating(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    def __str__(self):
        return f'{self.user.username} rated {self.song.title} - {self.rating}'
