import os
import shutil

import custom_io as io
from config import SONG_DIR, SONG_EXT
from entities import Playlist, Song
from repositories import file_repository, playlist_repository, song_repository
from services import youtube_api_service


def download_song(playlist: Playlist, song: Song) -> str:
    """Download song, convert downloaded file to the correct format, and set it as downloaded"""
    io.info("Downloading song")
    path = youtube_api_service.download_song(playlist, song)

    io.info("Normalizing the song and converting it to the correct format")
    filename = file_repository.normalize_and_convert_song_to_the_correct_format(path)

    print("Updating the song entry in the database")
    song_repository.set_song_as_downloaded(song, filename)

    return filename


def assert_song_has_no_playlist(original_playlist: Playlist, song: Song):
    """Check if song is in other playlist, if so then exit"""
    if not song_repository.song_exists(song.url):
        return

    updated_song = song_repository.get_song(song.url)
    if song_repository.song_has_playlist(updated_song):
        io.fatal(
            "Song %s is in multiple playlists (%s and %s), songs can only be in one playlist",
            updated_song,
            playlist_repository.get_song_playlist(updated_song),
            original_playlist,
        )


def rename_song(song: Song, artist: str, title: str) -> None:
    """Rename song to format artist - title and add the new data to the database"""
    new_filename = file_repository.get_song_filename(artist, title)
    song_repository.set_song_as_renamed(song, artist, title, new_filename)
    file_repository.rename_song(song, new_filename)
    file_repository.update_song_metadata(song, artist, title, new_filename)


def update_song_playlist(new_playlist: Playlist, song: Song) -> None:
    """Update song playlist"""
    song = song_repository.get_song(song.url)
    if song.downloaded:
        # Maybe print that the song has been moved?
        assert song.folder and song.filename
        original_path = os.path.join(SONG_DIR, song.folder, song.filename + SONG_EXT)
        target_path = os.path.join(
            SONG_DIR, new_playlist.filename, song.filename + SONG_EXT
        )
        shutil.move(original_path, target_path)

    song_repository.update_song_playlist(song, new_playlist)


def add_song(playlist: Playlist, song: Song) -> None:
    """Add song to playlist"""
    assert_song_has_no_playlist(playlist, song)

    if song_repository.song_exists(song.url):
        update_song_playlist(playlist, song)
    else:
        song_repository.add_song(playlist, song)
