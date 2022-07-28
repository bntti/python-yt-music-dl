import sys

from entities import Playlist
from services.youtube_api_service import youtube_api_service


class PlaylistService:
    """Handles adding and removing playlists and returns possible errors"""

    def get_remote_playlist(self, playlist_url: str) -> Playlist:
        """Check the URL and get the playlist from YouTube"""
        if "youtube.com/playlist?list=" not in playlist_url:
            sys.exit(f"Bad playlist URL: {playlist_url}")

        playlist = youtube_api_service.get_playlist(playlist_url)
        if not playlist:
            sys.exit(
                f"Failed to download playlist data for playlist with URL: {playlist_url}"
            )
        return playlist


playlist_service = PlaylistService()
