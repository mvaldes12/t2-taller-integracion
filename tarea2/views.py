from django.shortcuts import render, get_object_or_404

from . models import Artist, Album, Track
from . serializers import ArtistSerializer, AlbumSerializer, TrackSerializer

from rest_framework.views import APIView

from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

from base64 import b64encode


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the tarea2 index.")


@api_view(['GET', 'POST'])
def artist_list(request):

    if request.method == 'GET':
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        artist_data = request.data
        llaves = artist_data.keys()
        if "name" not in llaves or "age" not in llaves:
            return Response( status=status.HTTP_400_BAD_REQUEST)
        string = artist_data["name"]  
        #if string != str(string) or artist_data["age"] != int(artist_data["age"]):
        if type(string) != str or type(artist_data["age"]) != int:
            return Response( status=status.HTTP_400_BAD_REQUEST)

        id_encoded = b64encode(string.encode()).decode('utf-8')
        if len(id_encoded) >= 22:
            id_encoded = id_encoded[:22] 

        existe = Artist.objects.filter(id_artist = id_encoded)

        if existe:
            serializer = ArtistSerializer(existe[0])
            return Response(serializer.data , status=status.HTTP_409_CONFLICT)

        
        else:
            url_general = 'https://t2-taller-integracion-mvaldes.herokuapp.com/' 
            self_url = url_general + 'artist/' + id_encoded
            albums_url = self_url + '/albums'
            tracks_url = self_url + '/tracks'
            new_artist = Artist.objects.create(id_artist = id_encoded, name = artist_data["name"],
            age = artist_data["age"], albums_url = albums_url, tracks_url = tracks_url,
            self_url = self_url)
            new_artist.save()
            serializer = ArtistSerializer(new_artist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def album_list(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def new_album(request, id_artist):
    if request.method == 'POST':
        album_data = request.data
        llaves = album_data.keys()
        if "name" not in llaves or "genre" not in llaves:
            return Response( status=status.HTTP_400_BAD_REQUEST)
        nombre_album = album_data["name"]
        #if nombre_album != str(nombre_album) or type(album_data["genre"]) != str(album_data["genre"]):
        if type(nombre_album) != str or type(album_data["genre"]) != str:
            return Response( status=status.HTTP_400_BAD_REQUEST)

        string = nombre_album + ":" + id_artist
        id_encoded = b64encode(string.encode()).decode('utf-8')
        existe_artista = Artist.objects.filter(id_artist = id_artist)
        if existe_artista:
            artista = Artist.objects.get(id_artist=id_artist)
            serializer_artista = ArtistSerializer(artista)
        else:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if len(id_encoded) >= 22:
            id_encoded = id_encoded[:22] 

        existe = Album.objects.filter(id_album = id_encoded)
        if existe:
            serializer = AlbumSerializer(existe[0])
            return Response(serializer.data , status=status.HTTP_409_CONFLICT)
        
        else:
            url_general = 'https://t2-taller-integracion-mvaldes.herokuapp.com/'
            self_url = url_general + 'albums/' + id_encoded
            artist_url = url_general + 'artists/' + id_artist
            tracks_url = self_url + '/tracks'
            new_album = Album.objects.create(id_album = id_encoded, artist = artista , name = album_data["name"],
            genre = album_data["genre"], artist_url = artist_url ,tracks_url = tracks_url, self_url = self_url)
            new_album.save()
            serializer = AlbumSerializer(new_album)
            return Response(serializer.data,  status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        existe_artista = Artist.objects.filter(id_artist = id_artist)
        if existe_artista:
            artista = Artist.objects.get(id_artist=id_artist)
            albums = Album.objects.filter(artist = artista)
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def new_track(request, id_album):
    if request.method == 'POST':
        track_data = request.data
        llaves = track_data.keys()
        if "name" not in llaves or "duration" not in llaves:
            return Response( status=status.HTTP_400_BAD_REQUEST)
        nombre_track = track_data["name"]
        #if (nombre_track) != str(nombre_track) or (track_data["duration"]) != int((track_data["duration"])):
        if type(nombre_track) != str or type(track_data["duration"]) != float:
            return Response( status=status.HTTP_400_BAD_REQUEST)

        string = nombre_track + ":" + id_album
        id_encoded = b64encode(string.encode()).decode('utf-8')
        existe_album = Album.objects.filter(id_album = id_album)
        if existe_album:
            album = Album.objects.get(id_album=id_album)
            serializer_album = AlbumSerializer(album)
            artista_id = serializer_album.data["artist_id"]
        else:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if len(id_encoded) >= 22:
            id_encoded = id_encoded[:22] 

        existe = Track.objects.filter(id_track = id_encoded)
        if existe:
            serializer = TrackSerializer(existe[0])
            return Response(serializer.data , status=status.HTTP_409_CONFLICT)

        else:
            url_general = 'https://t2-taller-integracion-mvaldes.herokuapp.com/'
            self_url = url_general + 'tracks/' + id_encoded
            artist_url = url_general + 'artists/' + artista_id
            album_url = url_general + 'albums/' + id_album
            new_track = Track.objects.create(id_track = id_encoded, album = album , name = track_data["name"],
            duration = (track_data["duration"]), times_played = 0, artist_url = artist_url , album_url = album_url, self_url = self_url)
            new_track.save()
            serializer = TrackSerializer(new_track)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        existe_album = Album.objects.filter(id_album = id_album)
        if existe_album:
            album = Album.objects.get(id_album=id_album)
            tracks = Track.objects.filter(album = album)
            serializer = TrackSerializer(tracks, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET', 'POST'])
def track_list(request):
    if request.method == 'GET':
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
def artist_detail(request, id_artist):
    if request.method == 'GET':
        existe_artista = Artist.objects.filter(id_artist = id_artist)
        if existe_artista:
            artista = Artist.objects.get(id_artist=id_artist)
            serializer_artista = ArtistSerializer(artista)
            return Response(serializer_artista.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        existe_artista = Artist.objects.filter(id_artist = id_artist)
        if existe_artista:
            artista = Artist.objects.get(id_artist=id_artist)
            artista.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        

@api_view(['GET', 'PUT', 'DELETE'])
def album_detail(request, id_album):
    if request.method == 'GET':
        existe_album = Album.objects.filter(id_album = id_album)
        if existe_album:
            album = Album.objects.get(id_album=id_album)
            serializer_album = AlbumSerializer(album)
            return Response(serializer_album.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        existe_album = Album.objects.filter(id_album = id_album)
        if existe_album:
            album = Album.objects.get(id_album=id_album)
            album.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
@api_view(['GET', 'PUT', 'DELETE'])
def track_detail(request, id_track):
    if request.method == 'GET':
        existe_track = Track.objects.filter(id_track = id_track)
        if existe_track:
            track = Track.objects.get(id_track=id_track)
            serializer_track = TrackSerializer(track)
            return Response(serializer_track.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        existe_track = Track.objects.filter(id_track = id_track)
        if existe_track:
            track = Track.objects.get(id_track=id_track)
            track.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
@api_view(['GET', 'PUT', 'DELETE'])
def artist_tracks(request, id_artist):
    if request.method == 'GET':
        existe_artista = Artist.objects.filter(id_artist = id_artist)
        if existe_artista:
            artista = Artist.objects.get(id_artist=id_artist)
            albums = Album.objects.filter(artist=artista)
            lista = []
            for album in albums:
                tracks = Track.objects.filter(album = album)
                serializer = TrackSerializer(tracks, many=True)
                if tracks:
                    lista.append(serializer.data)
            return Response(lista[0])
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
def play_artist(request, id_artist):
    if request.method == 'PUT':
        existe_artista = Artist.objects.filter(id_artist = id_artist)
        if existe_artista:
            artista = Artist.objects.get(id_artist=id_artist)
            albums = Album.objects.filter(artist = artista)
            for album in albums:
                tracks = Track.objects.filter(album = album)
                for track in tracks:
                    track.times_played += 1
                    track_sumado = track.save()
                    serializer = TrackSerializer(track_sumado)
            return Response(status=status.HTTP_200_OK)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
def play_album(request, id_album):
    if request.method == 'PUT':
        existe_album = Album.objects.filter(id_album = id_album)
        if existe_album:
            album = Album.objects.get(id_album=id_album)
            tracks = Track.objects.filter(album = album)
            for track in tracks:
                track.times_played += 1
                track_sumado = track.save()
                serializer = TrackSerializer(track_sumado)
            return Response(status=status.HTTP_200_OK)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
def play_track(request, id_track):
    if request.method == 'PUT':
        existe_track = Track.objects.filter(id_track = id_track)
        if existe_track:
            track = Track.objects.get(id_track=id_track)
            track.times_played += 1
            track_sumado = track.save()
            serializer = TrackSerializer(track_sumado)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response( status=status.HTTP_405_METHOD_NOT_ALLOWED)