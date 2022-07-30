from colors import CLEAR, INFO
from entities import Song
from repositories import file_repository, song_repository
from services import youtube_api_service


def download_song(song: Song) -> str:
    """Download song, convert downloaded file to the correct format, and set it as downloaded"""
    print(f"{INFO}Downloading song{CLEAR}")
    path = youtube_api_service.download_song(song)

    print(f"{INFO}Normalizing the song and converting it to the correct format{CLEAR}")
    filename = file_repository.normalize_and_convert_song_to_the_correct_format(path)

    print(f"{INFO}Updating the song entry in the database{CLEAR}")
    song_repository.set_song_as_downloaded(song, filename)

    return filename
