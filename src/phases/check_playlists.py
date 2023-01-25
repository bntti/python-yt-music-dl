from typing import List

import custom_io as io
from config import CONFIG
from entities import Playlist
from repositories import playlist_repository, song_repository
from services import playlist_service, song_service, youtube_api_service


def check_for_removed_playlists(
    local_playlists: List[Playlist], remote_playlists: List[Playlist]
) -> None:
    """Check if any playlists have been removed"""
    to_be_removed = []
    for local_playlist in local_playlists:
        found = False
        for remote_playlist in remote_playlists:
            if local_playlist.url == remote_playlist.url:
                found = True
        if not found:
            to_be_removed.append(local_playlist)
    for playlist in to_be_removed:
        local_playlists.remove(playlist)
        playlist_repository.remove_playlist(playlist)


def check_removed_songs(remote_playlists: List[Playlist]) -> None:
    """Check for removed songs"""
    for remote_playlist in remote_playlists:
        if not playlist_repository.playlist_exists(remote_playlist):
            continue

        local_playlist = playlist_repository.get_playlist(remote_playlist.url)
        if local_playlist == remote_playlist:
            continue

        for song in local_playlist:
            if song not in remote_playlist:
                io.warn(
                    "Song %s has been removed from playlist %s", song, local_playlist
                )
                song_repository.remove_song_from_playlist(song)


def check_new_songs_or_playlists(remote_playlists: List[Playlist]) -> None:
    """Check for new playlists/songs"""
    for remote_playlist in remote_playlists:
        # Playlist doesn't exit locally
        if not playlist_repository.playlist_exists(remote_playlist):
            io.info("New playlist %s", remote_playlist)
            playlist_service.add_playlist(remote_playlist)
            continue

        # Playlist is OK
        local_playlist = playlist_repository.get_playlist(remote_playlist.url)
        if local_playlist.image_url != remote_playlist.image_url:
            playlist_repository.set_image_url(local_playlist, remote_playlist.image_url)
        if local_playlist == remote_playlist:
            continue

        # Check for new songs
        for song in remote_playlist:
            if song not in local_playlist:
                song_service.add_song(local_playlist, song)


def check_songs(remote_playlists: List[Playlist]) -> None:
    """Check for changes in playlist contents and for new playlists"""
    # We need to check for removed songs before checking for new songs
    # because songs may be moved from one playlist to another
    check_removed_songs(remote_playlists)
    check_new_songs_or_playlists(remote_playlists)


def check_playlists() -> None:
    """Check playlists for changes and return True if there are changes"""
    urls = CONFIG["playlist_urls"]

    io.title("Checking the playlists")
    io.subtitle("Downloading the playlist data from YouTube")
    remote_playlists = []
    for i, url in enumerate(urls):
        io.info(f"Downloading playlist data ({i+1}/{len(urls)})")
        remote_playlists.append(youtube_api_service.get_playlist(url))
    local_playlists = playlist_repository.get_playlists()

    io.subtitle("Checking the playlists")
    check_for_removed_playlists(local_playlists, remote_playlists)
    check_songs(remote_playlists)
