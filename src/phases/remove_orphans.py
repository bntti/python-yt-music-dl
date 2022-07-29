from colors import CLEAR, TITLE
from repositories import file_repository, song_repository


def remove_orphans():
    songs = song_repository.get_songs()
    print(f"{TITLE}Removing orphans{CLEAR}")
    for song in songs:
        if not song_repository.song_has_playlist(song):
            song_repository.remove_song(song)
            file_repository.delete_song_file(song)
