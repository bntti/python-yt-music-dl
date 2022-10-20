import sys

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from colors import CLEAR, ERROR, ITALIC, WARN
from config import SONG_DIR
from entities import Playlist, Song


def song_download_fail(song_url: str):
    sys.exit(f"{ERROR}Unable to get song data for song with URL: {song_url}{CLEAR}")


def playlist_download_fail(playlist_url: str):
    sys.exit(
        f"{ERROR}Failed to download playlist data for playlist with URL: {playlist_url}{CLEAR}",
    )


def get_song_thumbnail_url(song_url: str) -> str:
    try:
        ydl_opts = {"skip_download": True, "quiet": True}
        with YoutubeDL(ydl_opts) as ydl:
            song = ydl.extract_info(song_url)
    except DownloadError:
        song_download_fail(song_url)
    if song is None:
        song_download_fail(song_url)

    song_url = ""
    maxsize = 0
    for x in song["thumbnails"]:
        if "resolution" in x:
            if int(x["height"] > maxsize):
                maxsize = int(x["height"])
                song_url = x["url"]
    return song_url


def get_playlist(playlist_url: str) -> Playlist:
    """Downloads playlist data from YouTube and
    returns a Playlist object and None if the download failed
    """
    if "youtube.com/playlist?list=" not in playlist_url:
        sys.exit(f"{ERROR}Bad playlist URL: {playlist_url}{CLEAR}")

    try:
        ydl_opts = {"extract_flat": "in_playlist", "quiet": True}
        with YoutubeDL(ydl_opts) as ydl:
            playlist = ydl.extract_info(playlist_url)
    except DownloadError:
        playlist_download_fail(playlist_url)
    if playlist is None:
        playlist_download_fail(playlist_url)

    songs = []
    for song in playlist["entries"]:
        if song["uploader"] is None:
            sys.exit(
                f"{ERROR}There is an invalid song in playlist {ITALIC}{playlist['title']}{ERROR}, "
                f"you should remove it from the playlist to continue{CLEAR}",
            )
        songs.append(
            Song(
                song["url"],
                song["uploader"],
                song["title"],
                song["duration"],
            )
        )

    is_album = len(playlist["thumbnails"]) == 3

    return Playlist(
        playlist["webpage_url"],
        playlist["title"],
        get_song_thumbnail_url(songs[0].url),
        is_album,
        songs,
    )


def download_song(song: Song) -> str:
    """Downloads the song file and returns the file path"""
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": {"default": "%(title)s.%(ext)s"},
        "paths": {"home": SONG_DIR},
        "quiet": True,
    }
    failed_attempts = 0
    while True:
        with YoutubeDL(ydl_opts) as ydl:
            try:
                song_data = ydl.extract_info(song.url)
                return ydl.prepare_filename(song_data)
            except DownloadError:
                failed_attempts += 1
                if failed_attempts == 3:
                    sys.exit(
                        f"{ERROR}Failed to download song {ITALIC}{song}{ERROR}, "
                        f"you should remove it from it's playlist to download the songs{CLEAR}",
                    )
                else:
                    print(
                        f"{WARN}Failed to download song {ITALIC}{song}{CLEAR}, retrying"
                    )
