from entities import Playlist
from repositories import playlist_repository
from services import song_service


def add_playlist(playlist: Playlist) -> None:
    """Check playlist for duplicate songs and then add the playlist to the database"""
    for song in playlist:
        song_service.assert_song_has_no_playlist(playlist, song)

    playlist_repository.add_playlist(playlist)
    for song in playlist:
        song_service.add_song(playlist, song)
