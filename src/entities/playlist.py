from typing import List

from entities.song import Song


class Playlist:
    """Playlist object, matches a playlist on YouTube.

    Attributes:
        url (str): Playlist Youtube url
        title (str): Playlist title
        songs (List[Song]): Songs that the playlist contains
    """

    def __init__(self, url: str, title: str, image_url: str, songs: List[Song]) -> None:
        """Playlist object constructor

        Args:
            url (str): Playlist Youtube url
            title (str): Playlist title
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

    def __eq__(self, other: "Playlist") -> bool:
        for song in self.songs:
            if song not in other.songs:
                return False
        for song in other.songs:
            if song not in self.songs:
                return False

        return self.url == other.url and self.title == other.title

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"Playlist({self.url}, {self.title}, {repr(self.songs)})"
