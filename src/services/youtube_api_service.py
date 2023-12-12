from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

import custom_io as io
from config import SONG_DIR
from entities import Playlist, Song
from repositories import file_repository, song_repository


def get_song_thumbnail_url(song_url: str) -> str:
    """Get the highest resolution thumbnail image for song"""
    try:
        ydl_opts = {"skip_download": True, "quiet": True}
        with YoutubeDL(ydl_opts) as ydl:
            song = ydl.extract_info(song_url)
    except DownloadError:
        io.fatal("Unable to get song data for song with URL %s", song_url)
    if song is None:
        io.fatal("Unable to get song data for song with URL %s", song_url)

    song_url = ""
    maxsize = 0
    for thumbnail in song["thumbnails"]:
        if "resolution" in thumbnail:
            if int(thumbnail["height"] > maxsize):
                maxsize = int(thumbnail["height"])
                song_url = thumbnail["url"]
    return song_url


def get_playlist(playlist_url: str) -> Playlist:
    """Downloads playlist data from YouTube and
    returns a Playlist object and None if the download failed
    """
    if "youtube.com/playlist?list=" not in playlist_url:
        io.fatal("Bad playlist URL: %s", playlist_url)

    try:
        ydl_opts = {"extract_flat": "in_playlist", "quiet": True}
        with YoutubeDL(ydl_opts) as ydl:
            playlist = ydl.extract_info(playlist_url)
    except DownloadError:
        io.fatal(
            "Failed to download playlist data for playlist with URL: %s", playlist_url
        )
    if playlist is None:
        io.fatal(
            "Failed to download playlist data for playlist with URL: %s", playlist_url
        )

    songs = []
    for song in playlist["entries"]:
        if song["channel"] is None:
            io.warn(
                "There is an invalid song in playlist %s, "
                + "you should remove it from the playlist. Skipping it for now",
                playlist["title"],
            )
            if song["url"] and song_repository.song_exists(song["url"]):
                song = song_repository.get_song(song["url"])
                io.info(
                    "Url: %s\nYT data: %s - %s\nRenamed: %s - %s",
                    song.url,
                    song.uploader,
                    song.yt_title,
                    song.artist,
                    song.title,
                )
            continue
        songs.append(
            Song(
                song["url"],
                song["channel"],
                song["title"],
                song["duration"],
            )
        )

    filename = file_repository.sanitize_filename(playlist["title"])
    file_repository.create_playlist_folder(filename)

    return Playlist(
        playlist["webpage_url"],
        playlist["title"],
        get_song_thumbnail_url(songs[0].url),
        filename,
        songs,
    )


def download_song(playlist: Playlist, song: Song) -> str:
    """Downloads the song file and returns the file path"""
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": {"default": "%(title)s.%(ext)s"},
        "paths": {"home": f"{SONG_DIR}/{playlist.filename}"},
        "quiet": True,
    }
    for _ in range(3):
        with YoutubeDL(ydl_opts) as ydl:
            try:
                song_data = ydl.extract_info(song.url)
                return ydl.prepare_filename(song_data)
            except DownloadError:
                io.warn("Failed to download song %s, retrying", song)

    io.fatal(
        "Failed to download song %s, you should remove it from it's playlist "
        + "to download the songs or try again",
        song,
    )
