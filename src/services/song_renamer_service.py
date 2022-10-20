from pathvalidate import sanitize_filepath

from colors import CLEAR, WARN
from entities import Song
from repositories import file_repository, song_repository


def rename_song(song: Song, artist: str, title: str) -> None:
    """Rename song to format artist - title and add the new data to the database"""
    new_filename = str(sanitize_filepath(f"{artist} - {title}"))
    new_filename = new_filename.replace("/", "")

    filename_exists = song_repository.filename_exists(new_filename, song)
    if song.filename != new_filename and filename_exists:
        print(
            f"{WARN}Another song with same filename exists, "
            f"adding _<number> to the end of the filename{CLEAR}"
        )
        num = 2
        original_filename = new_filename
        while song_repository.filename_exists(new_filename, song):
            new_filename = f"{original_filename}_{num}"

    song_repository.set_song_as_renamed(song, artist, title, new_filename)
    file_repository.rename_song(song, new_filename)
    file_repository.update_song_metadata(song, artist, title, new_filename)
