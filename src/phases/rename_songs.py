from typing import List

from colors import CLEAR, INFO, ITALIC, SUBTITLE, TITLE
from entities import Song
from repositories import song_repository
from services import song_renamer_service


def _rename_songs(songs: List[Song], not_renamed: List[Song]) -> None:
    """Rename the songs in the not_renamed list using user input"""
    for i, song in enumerate(not_renamed):
        print(f"{SUBTITLE}Renaming song {i+1}/{len(songs)}{CLEAR}")
        print(f"Uploader '{song.uploader}'\nTitle: '{song.yt_title}'")

        artist = song.uploader
        title = song.yt_title
        if " - " in song.yt_title:
            artist, title = song.yt_title.split(" - ")[0:2]
        input_artist = input(f"Song artist [{ITALIC}{artist}{CLEAR}]: ")
        input_title = input(f"Song title [{ITALIC}{title}{CLEAR}]: ")
        artist = input_artist if input_artist else artist
        title = input_title if input_title else title

        song_renamer_service.rename_song(song, artist, title)


def rename_songs():
    """Rename songs that have not been downloaded yet using user input"""
    songs = song_repository.get_songs()
    print(f"{TITLE}Renaming songs{CLEAR}")

    not_renamed = []
    for song in songs:
        if song.renamed:
            continue

        album_count = song_repository.album_count(song)
        pl_count = song_repository.playlist_count(song)
        if album_count == 0 and pl_count == 0:
            continue

        not_renamed.append(song)

    if len(not_renamed) == 0:
        print(f"{INFO}All songs have been renamed{CLEAR}")

    _rename_songs(songs, not_renamed)
