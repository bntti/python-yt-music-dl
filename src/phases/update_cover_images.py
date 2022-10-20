from colors import CLEAR, TITLE
from repositories import file_repository, playlist_repository


def update_cover_images() -> None:
    print(f"{TITLE}Updating cover images{CLEAR}")
    playlists = playlist_repository.get_playlists()
    for playlist in playlists:
        file_repository.write_cover_images(playlist)
