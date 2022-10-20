import custom_io as io
from entities import Song
from repositories import file_repository, song_repository
from services import youtube_api_service


def download_song(song: Song) -> str:
    """Download song, convert downloaded file to the correct format, and set it as downloaded"""
    io.info("Downloading song")
    path = youtube_api_service.download_song(song)

    io.info("Normalizing the song and converting it to the correct format")
    filename = file_repository.normalize_and_convert_song_to_the_correct_format(path)

    print("Updating the song entry in the database")
    song_repository.set_song_as_downloaded(song, filename)

    return filename
