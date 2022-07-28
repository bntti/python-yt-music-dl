import sys

from config import CONFIG
from repositories import playlist_repository
from services import playlist_service


def check_playlists():
    urls = CONFIG["songs"]
    if len(urls) == 0:
        sys.exit("No playlists to download, exiting")

    remote_playlists = []
    for url in urls:
        remote_playlists.append(playlist_service.get_remote_playlist(url))

    # Check if playlists have been removed
    local_playlists = playlist_repository.get_playlists()
    to_be_removed = []
    for local_playlist in local_playlists:
        found = False
        for remote_playlist in remote_playlists:
            if local_playlist.url == remote_playlist.url:
                found = True
        if not found:
            to_be_removed.append(local_playlist)
    for playlist in to_be_removed:
        playlist_repository.remove_playlist(playlist)

    # Check if remote playlists are different than the local ones
    for remote_playlist in remote_playlists:
        # Playlist doesn't exit locally
        if not playlist_repository.playlist_exists(remote_playlist):
            print(f"New playlist '{remote_playlist}'")
            playlist_repository.add_playlist(remote_playlist)
            continue

        # Playlist is OK
        local_playlist = playlist_repository.get_playlist(remote_playlist.url)
        if local_playlist == remote_playlist:
            continue

        # Check for removed songs
        for song in local_playlist:
            if song not in remote_playlist:
                print(
                    f"Song '{song}' has been removed from playlist '{local_playlist}'"
                )
                playlist_repository.remove_song_from_playlist(local_playlist, song)

        # Check for new songs
        for song in remote_playlist:
            if song not in local_playlist:
                playlist_repository.add_song_to_playlist(local_playlist, song)
