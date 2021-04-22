from django.db import models

# Create your models here.

class Artist(models.Model):
    id_artist = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    albums_url = models.URLField()
    tracks_url = models.URLField()
    self_url = models.URLField()


class Album(models.Model):
    id_album = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    artist_url = models.URLField()
    tracks_url = models.URLField()
    self_url = models.URLField()

class Track(models.Model):
    id_track = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    duration = models.FloatField()
    times_played = models.IntegerField()
    artist_url = models.URLField()
    album =  models.ForeignKey(Album, on_delete=models.CASCADE)
    album_url = models.URLField()
    self_url = models.URLField()

