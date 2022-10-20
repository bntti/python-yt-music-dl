import custom_io as io
from repositories import file_repository, playlist_repository


def update_cover_images() -> None:
    """Update the playlist cover image and update cover images of all the songs"""
    io.title("Updating cover images")
    playlists = playlist_repository.get_playlists()
    for playlist in playlists:
        file_repository.write_cover_images(playlist)
