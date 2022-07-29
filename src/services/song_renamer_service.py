from pathvalidate import sanitize_filepath

from colors import CLEAR, WARN
from entities import Song
from repositories import file_repository, song_repository


class SongRenamerService:
    """Renames songs to format "Artist - Title" by using user input"""

    def rename_song(self, song: Song, artist: str, title: str) -> None:
        """Rename song to format artist - title and add the new data to the database"""
        new_filename = sanitize_filepath(f"{artist} - {title}")
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
        file_repository.write_song_tags(song, artist, title, new_filename)


song_renamer_service = SongRenamerService()
