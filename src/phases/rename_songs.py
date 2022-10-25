from typing import List

import custom_io as io
from entities import Song
from repositories import song_repository
from services import song_service


def _rename_songs(not_renamed: List[Song]) -> None:
    """Rename the songs in the not_renamed list using user input"""
    for i, song in enumerate(not_renamed):
        io.subtitle(f"Renaming song {i+1}/{len(not_renamed)}")
        io.info("Uploader %s\nTitle: %s", song.uploader, song.yt_title)

        artist = song.uploader
        title = song.yt_title
        if " - " in song.yt_title:
            artist, title = song.yt_title.split(" - ")[0:2]
        input_artist = io.inpt("Song artist [%s]: ", artist)
        input_title = io.inpt("Song title [%s]: ", title)
        artist = input_artist if input_artist else artist
        title = input_title if input_title else title

        song_service.rename_song(song, artist, title)


def rename_songs() -> None:
    """Rename songs that have not been downloaded yet using user input"""
    songs = song_repository.get_songs()
    io.title("Renaming songs")

    not_renamed = [song for song in songs if not song.renamed and song.downloaded]
    if len(not_renamed) == 0:
        io.info("All songs have been renamed")
    else:
        _rename_songs(not_renamed)
