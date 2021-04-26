from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('artists', views.artist_list),
    path('albums', views.album_list),
    path('tracks', views.track_list),
    path('artists/<str:id_artist>', views.artist_detail),
    path('albums/<str:id_album>', views.album_detail),
    path('tracks/<str:id_track>', views.track_detail),
    path('albums/<str:id_album>/tracks', views.new_track),
    path('artists/<str:id_artist>/albums', views.new_album),
    path('artists/<str:id_artist>/tracks', views.artist_tracks),
    path('artists/<str:id_artist>/albums/play', views.play_artist),
    path('albums/<str:id_album>/tracks/play', views.play_album),
    path('tracks/<str:id_track>/play', views.play_track),

]