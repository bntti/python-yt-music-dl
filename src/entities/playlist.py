from typing import List

from entities.song import Song


class Playlist:
    """Playlist object, matches a playlist on YouTube.

    Attributes:
        url (str): Playlist Youtube url
        title (str): Playlist title
        image_url (str): URL of the cover image used for the songs in this playlist
        songs (List[Song]): Songs that the playlist contains
    """

    def __init__(self, url: str, title: str, image_url: str, songs: List[Song]) -> None:
        """Playlist object constructor

        Args:
            url (str): Playlist Youtube url
            title (str): Playlist title
            image_url (str): URL of the cover image used for the songs in this playlist
            songs (List[Song]): Songs that the playlist contains
        """
        self.url = url
        self.title = title
        self.image_url = image_url
        self.songs = songs

        self.song_index = 0

    def __contains__(self, song: Song) -> bool:
        for pl_song in self.songs:
            if pl_song.url == song.url:
                return True
        return False

    def __iter__(self) -> "Playlist":
        self.song_index = 0
        return self

    def __next__(self) -> Song:
        if self.song_index >= len(self.songs):
            raise StopIteration

        self.song_index += 1
        return self.songs[self.song_index - 1]

    def __getitem__(self, index: int) -> "Song":
        if index < 0 or index >= len(self.songs):
            raise Exception(f"Invalid song index {index} for playlist {self.title}")
        return self.songs[index]

    def __str__(self) -> str:
        return self.title
