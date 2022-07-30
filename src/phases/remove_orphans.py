from colors import CLEAR, ITALIC, TITLE, WARN
from repositories import file_repository, song_repository


def remove_orphans():
    """Remove songs that are not in any playlist"""
    songs = song_repository.get_songs()
    print(f"{TITLE}Removing orphans{CLEAR}")
    for song in songs:
        if not song_repository.song_has_playlist(song):
            print(
                f"{WARN}Removing song {ITALIC}{song}{WARN}",
                f"file because it isn't in any playlist{CLEAR}",
            )
            song_repository.remove_song(song)
            if song.downloaded:
                file_repository.delete_song_file(song)
