from django.db import models
from django.urls import reverse

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('song_detail', kwargs={'pk': self.pk})
        