import custom_io as io
from repositories import file_repository, song_repository


def remove_orphans() -> None:
    """Remove songs that are not in any playlist"""
    songs = song_repository.get_songs()
    io.title("Removing orphans")
    for song in songs:
        if not song_repository.song_has_playlist(song):
            io.warn("Removing song %s because it isn't in any playlist", song)
            song_repository.remove_song(song)
            if song.downloaded:
                file_repository.delete_song_file(song)
