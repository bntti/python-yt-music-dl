from colors import CLEAR, INFO
from entities import Song
from repositories import file_repository, song_repository
from services.youtube_api_service import youtube_api_service


class SongService:
    """Handles songs"""

    def download_song(self, song: Song) -> str:
        """Download song, convert downloaded file to the correct format, and set it as downloaded"""
        print(f"{INFO}Downloading song{CLEAR}")
        path = youtube_api_service.download_song(song)

        print(f"{INFO}Normalizing and converting song to the correct format{CLEAR}")
        filename = file_repository.normalize_and_convert_song_to_the_correct_format(
            path
        )

        print(f"{INFO}Updating database{CLEAR}")
        song_repository.set_song_as_downloaded(song, filename)

        return filename


song_service = SongService()
