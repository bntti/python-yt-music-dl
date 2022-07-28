import sys

from repositories import file_repository, playlist_repository, song_repository
from services import song_service


def download_songs():
    songs = song_repository.get_songs()
    print("Going through songs")
    for i, song in enumerate(songs):
        print(f"Going through song {i+1}/{len(songs)}")

        pl_count = song_repository.playlist_count(song)
        if pl_count == 0:
            continue
        if pl_count > 1:
            sys.exit(f"Song {song} is in more than one playlist")
        playlist = playlist_repository.get_song_playlist(song)

        # Download song
        if not song.downloaded:
            filename = song_service.download_song(song)
            song.filename = filename

        # Check song tag
        file_repository.check_song_album(song, playlist)
