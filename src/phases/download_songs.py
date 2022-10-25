import custom_io as io
from repositories import file_repository, playlist_repository, song_repository
from services import song_service


def download_songs() -> None:
    """Download songs that have not been downloaded yet and write some metadata to them"""
    songs = song_repository.get_songs()
    io.title("Downloading songs")
    not_downloaded = []
    for song in songs:
        playlist = playlist_repository.get_song_playlist(song)

        if not song.downloaded:
            not_downloaded.append((song, playlist))

    if len(not_downloaded) == 0:
        io.info("All songs have been downloaded")

    for i, (song, playlist) in enumerate(not_downloaded):
        io.subtitle(f"Downloading song {i+1}/{len(not_downloaded)}")
        filename = song_service.download_song(song)
        song.filename = filename

        io.info("Writing song metadata")
        file_repository.write_song_metadata(song, playlist)

    io.subtitle("Updating cover images")
    for playlist in playlist_repository.get_playlists():
        file_repository.write_cover_images(playlist)
