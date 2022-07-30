import sys

from colors import CLEAR, ERROR
from entities import Playlist
from services import youtube_api_service


def get_remote_playlist(playlist_url: str) -> Playlist:
    """Check the URL and get the playlist from YouTube"""
    if "youtube.com/playlist?list=" not in playlist_url:
        sys.exit(f"{ERROR}Bad playlist URL: {playlist_url}{CLEAR}")

    playlist = youtube_api_service.get_playlist(playlist_url)
    if not playlist:
        sys.exit(
            f"{ERROR}Failed to download playlist data ",
            f"for playlist with URL: {playlist_url}{CLEAR}",
        )
    return playlist
