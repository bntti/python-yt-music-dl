import sys

from colors import CLEAR, ERROR, INFO, SUBTITLE, TITLE
from repositories import file_repository, playlist_repository, song_repository
from services import song_service


def download_songs():
    """Download songs that have not been downloaded yet and write some metadata to them"""
    songs = song_repository.get_songs()
    print(f"{TITLE}Downloading songs{CLEAR}")
    not_downloaded = []
    for song in songs:
        album_count = song_repository.album_count(song)
        pl_count = song_repository.playlist_count(song)
        if album_count == 0 and pl_count == 0:
            continue

        if album_count > 1:
            sys.exit(f"{ERROR}Song {song} is in more than one album{CLEAR}")
        elif album_count == 0 and pl_count > 1:
            sys.exit(f"{ERROR}Song {song} is in more than one playlist{CLEAR}")
        elif album_count == 1:
            playlist = playlist_repository.get_song_album(song)
        else:
            playlist = playlist_repository.get_song_playlist(song)

        if not song.downloaded:
            not_downloaded.append((song, playlist))

    if len(not_downloaded) == 0:
        print(f"{INFO}All songs have been downloaded{CLEAR}")

    for i, (song, playlist) in enumerate(not_downloaded):
        print(f"{SUBTITLE}Downloading song {i+1}/{len(not_downloaded)}{CLEAR}")
        filename = song_service.download_song(song)
        song.filename = filename

        print(f"{INFO}Writing song metadata{CLEAR}")
        file_repository.write_song_metadata(song, playlist)
