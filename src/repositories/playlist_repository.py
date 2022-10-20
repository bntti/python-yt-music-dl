from typing import List

from database_connection import get_database_connection
from entities import Playlist, Song
from repositories.song_repository import song_repository


class PlaylistRepository:
    """Handles saving playlist objects to the database"""

    def __init__(self) -> None:
        self._connection = get_database_connection()

    def get_playlists(self) -> List[Playlist]:
        """Fetches a list of all the playlists from the database"""
        cursor = self._connection.cursor()
        cursor.execute("SELECT url, title, image_url, is_album FROM playlists")
        rows = cursor.fetchall()

        playlists = []
        for row in rows:
            songs = self.get_playlist_songs(row["url"])
            playlist = Playlist(
                row["url"], row["title"], row["image_url"], row["is_album"], songs
            )
            playlists.append(playlist)
        return playlists

    def get_playlist(self, url: str) -> Playlist:
        """Fetches the playlist with the corresponding url. Returns None if one doesn't exist"""
        cursor = self._connection.cursor()
        sql = "SELECT url, title, image_url, is_album FROM playlists WHERE url = ?"
        cursor.execute(sql, [url])
        row = cursor.fetchone()

        if not row:
            raise Exception(f"No playlist exists with url {url}")

        songs = self.get_playlist_songs(row["url"])
        return Playlist(
            row["url"], row["title"], row["image_url"], row["is_album"], songs
        )

    def get_playlist_songs(self, playlist_url: str) -> List[Song]:
        """Fetches the list of songs that are in the specified playlist"""
        sql = """SELECT s.*
                 FROM songs s, playlist_songs ps
                 WHERE ps.playlist_url = ? AND ps.song_url = s.url"""
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist_url])
        rows = cursor.fetchall()
        return [song_repository.row_to_song(row) for row in rows]

    def get_song_album(self, song: Song) -> Playlist:
        """Get the album that the song is in"""
        sql = """SELECT p.url, p.title, p.image_url, p.is_album
                 FROM playlists p, playlist_songs ps
                 WHERE p.is_album = true AND ps.playlist_url = p.url AND ps.song_url = ?"""
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        row = cursor.fetchone()
        return Playlist(
            row["url"],
            row["title"],
            row["image_url"],
            row["is_album"],
            self.get_playlist_songs(row["url"]),
        )

    def get_song_playlist(self, song: Song) -> Playlist:
        """Get the playlist that the song is in"""
        sql = """SELECT p.url, p.title, p.image_url, p.is_album
                 FROM playlists p, playlist_songs ps
                 WHERE p.is_album = false AND ps.playlist_url = p.url AND ps.song_url = ?"""
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        row = cursor.fetchone()
        return Playlist(
            row["url"],
            row["title"],
            row["image_url"],
            row["is_album"],
            self.get_playlist_songs(row["url"]),
        )

    def playlist_exists(self, playlist: Playlist) -> bool:
        """Check if a playlist with the specified url is in the database"""
        sql = "SELECT 1 FROM playlists WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist.url])
        return bool(cursor.fetchone())

    def add_playlist(self, playlist: Playlist) -> None:
        """Add a playlist to the database"""
        sql = "INSERT INTO playlists (url, title, image_url, is_album) VALUES (?, ?, ?, ?)"
        cursor = self._connection.cursor()
        cursor.execute(
            sql, [playlist.url, playlist.title, playlist.image_url, playlist.is_album]
        )
        self._connection.commit()

        for song in playlist:
            self.add_song_to_playlist(playlist, song)

    def add_song_to_playlist(self, playlist: Playlist, song: Song) -> None:
        """Adds a song to the playlist"""
        song_repository.add_song(song)

        sql = "INSERT INTO playlist_songs (playlist_url, song_url) VALUES (?, ?)"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist.url, song.url])
        self._connection.commit()

    def remove_playlist(self, playlist: Playlist) -> None:
        """Removes a playlist from the database"""
        sql = "DELETE FROM playlists WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist.url])
        self._connection.commit()

    def remove_song_from_playlist(self, playlist: Playlist, song: Song) -> None:
        """Removes a playlist from the playlist"""
        sql = "DELETE FROM playlist_songs WHERE playlist_url = ? AND song_url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist.url, song.url])
        self._connection.commit()


playlist_repository = PlaylistRepository()
