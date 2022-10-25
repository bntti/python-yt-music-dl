from typing import Dict, List

from database_connection import get_database_connection
from entities import Playlist, Song
from repositories.song_repository import song_repository


class PlaylistRepository:
    """Handles saving playlist objects to the database"""

    def __init__(self) -> None:
        self._connection = get_database_connection()

    def create_playlist(self, row: Dict[str, str], songs: List[Song]) -> Playlist:
        """Create playlist object from row object and the list of songs"""
        return Playlist(
            row["url"], row["title"], row["image_url"], row["filename"], songs
        )

    def get_playlists(self) -> List[Playlist]:
        """Fetches a list of all the playlists from the database"""
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM playlists")
        rows = cursor.fetchall()

        playlists = []
        for row in rows:
            songs = song_repository.get_playlist_songs(row["url"])
            playlist = self.create_playlist(row, songs)
            playlists.append(playlist)
        return playlists

    def get_playlist(self, url: str) -> Playlist:
        """Fetches the playlist with the corresponding url. Returns None if one doesn't exist"""
        cursor = self._connection.cursor()
        sql = "SELECT * FROM playlists WHERE url = ?"
        cursor.execute(sql, [url])
        row = cursor.fetchone()

        if not row:
            raise Exception(f"Tried to get playlist that does not exist (URL: {url})")

        songs = song_repository.get_playlist_songs(row["url"])
        return self.create_playlist(row, songs)

    def get_song_playlist(self, song: Song) -> Playlist:
        """Get the playlist that the song is in"""
        sql = """SELECT p.*
                 FROM playlists p, songs s
                 WHERE s.playlist_url = p.url AND s.url = ?"""
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        row = cursor.fetchone()

        if not row:
            raise Exception(
                f"Tried to get playlist for song that does not have a playlist (song: {song})"
            )

        return self.create_playlist(row, song_repository.get_playlist_songs(row["url"]))

    def playlist_exists(self, playlist: Playlist) -> bool:
        """Check if a playlist with the specified url is in the database"""
        sql = "SELECT 1 FROM playlists WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist.url])
        return bool(cursor.fetchone())

    def filename_exists(self, filename: str) -> bool:
        """Check if playlist with folder filename exists"""
        sql = "SELECT 1 FROM playlists WHERE filename = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [filename])
        return bool(cursor.fetchone())

    def add_playlist(self, playlist: Playlist) -> None:
        """Add a playlist to the database but not it's songs"""
        sql = "INSERT INTO playlists (url, title, image_url, filename) VALUES (?, ?, ?, ?)"
        cursor = self._connection.cursor()
        cursor.execute(
            sql, [playlist.url, playlist.title, playlist.image_url, playlist.filename]
        )
        self._connection.commit()

    def remove_playlist(self, playlist: Playlist) -> None:
        """Removes a playlist from the database"""
        sql = "DELETE FROM playlists WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist.url])
        self._connection.commit()


playlist_repository = PlaylistRepository()
