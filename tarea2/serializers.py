from rest_framework import serializers 
from tarea2.models import Artist, Album, Track
 
 
class ArtistSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField("id_artist")
    albums = serializers.SerializerMethodField("albums_url")
    tracks = serializers.SerializerMethodField("tracks_url")
    self = serializers.SerializerMethodField("self_url")
    
    class Meta:
        model = Artist
        fields = ('id',
                  'name',
                  'age',
                  'albums',
                  'tracks',
                  'self')

    def id_artist(self, objeto):
        return objeto.id_artist

    def albums_url(self, objeto):
        return objeto.albums_url
    
    def tracks_url(self, objeto):
        return objeto.tracks_url

    def self_url(self, objeto):
        return objeto.self_url


class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField("id_album")
    artist_id = serializers.SerializerMethodField("id_artist")
    artist = serializers.SerializerMethodField("artist_url")
    tracks = serializers.SerializerMethodField("tracks_url")
    self = serializers.SerializerMethodField("self_url")
    class Meta:
        model = Album
        fields = ('id',
                  'artist_id',
                  'name',
                  'genre',
                  'artist',
                  'tracks',
                  'self')            

    def id_album(self, objeto):
        return objeto.id_album

    def id_artist(self, objeto):
        return objeto.artist.id_artist

    def artist_url(self, objeto):
        return objeto.artist_url

    def tracks_url(self, objeto):
        return objeto.tracks_url

    def self_url(self, objeto):
        return objeto.self_url

class TrackSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField("id_track")
    album_id = serializers.SerializerMethodField("id_album")
    artist = serializers.SerializerMethodField("artist_url")
    album = serializers.SerializerMethodField("album_url")
    self = serializers.SerializerMethodField("self_url")
    class Meta:
        model = Track
        fields = ('id',
                  'album_id',
                  'name',
                  'duration',
                  'times_played',
                  'artist',
                  'album',
                  'self')  

    def id_track(self, objeto):
        return objeto.id_track

    def id_album(self, objeto):
        return objeto.album.id_album

    def artist_url(self, objeto):
        return objeto.artist_url

    def album_url(self, objeto):
        return objeto.album_url

    def self_url(self, objeto):
        return objeto.self_url


  
