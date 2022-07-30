import sys
from typing import Optional

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from colors import CLEAR, ERROR, ITALIC
from config import SONG_DIR
from entities import Playlist, Song


class YoutubeApiService:
    """Handles downloading data from YouTube"""

    @staticmethod
    def get_playlist(playlist_url: str) -> Optional[Playlist]:
        """Downloads playlist data from YouTube and
        returns a Playlist object and None if the download failed
        """
        try:
            ydl_opts = {"extract_flat": "in_playlist", "quiet": True}
            with YoutubeDL(ydl_opts) as ydl:
                playlist = ydl.extract_info(playlist_url)
        except DownloadError:
            return None

        songs = []
        for song in playlist["entries"]:
            songs.append(
                Song(
                    song["url"],
                    song["uploader"],
                    song["title"],
                    song["thumbnails"][3]["url"],
                    song["duration"],
                )
            )

        is_album = len(playlist["thumbnails"]) == 3
        thumbnail_id = 1 if is_album else 3

        return Playlist(
            playlist["webpage_url"],
            playlist["title"],
            playlist["thumbnails"][thumbnail_id]["url"],
            is_album,
            songs,
        )

    @staticmethod
    def download_song(song: Song) -> str:
        """Downloads the song file and returns the file path"""
        ydl_opts = {
            "format": "bestaudio",
            "outtmpl": {"default": "%(title)s.%(ext)s"},
            "paths": {"home": SONG_DIR},
            "quiet": True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            try:
                song_data = ydl.extract_info(song.url)
            except DownloadError:
                sys.exit(
                    f"{ERROR}Failed to download song {ITALIC}{song}{ERROR}, "
                    f"you should remove it from it's playlist to download the songs{CLEAR}",
                )
            return ydl.prepare_filename(song_data)


youtube_api_service = YoutubeApiService()
