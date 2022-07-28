import sqlite3
from typing import List, Optional

from database_connection import get_database_connection
from entities import Playlist, Song


class SongRepository:
    """Handles saving song objects to the database"""

    def __init__(self):
        self._connection = get_database_connection()

    @staticmethod
    def row_to_song(row: list) -> Song:
        """Convert a SQL row object to a Song object"""
        return Song(
            row["url"],
            row["uploader"],
            row["yt_title"],
            row["image_url"],
            row["length"],
            row["downloaded"],
            row["filename"],
            row["renamed"],
            row["artist"],
            row["title"],
        )

    def get_songs(self) -> List[Song]:
        """Fetches a list of all the songs in the database"""
        sql = "SELECT * FROM songs ORDER BY downloaded DESC, LOWER(filename), LOWER(yt_title)"
        cursor = self._connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [self.row_to_song(row) for row in rows]

    def playlist_count(self, song: Song) -> int:
        """Return the number of playlists that contain the song"""
        sql = """SELECT COUNT(*) FROM playlist_songs WHERE song_url = ?"""
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        row = cursor.fetchone()
        return int(row[0])

    def song_has_playlist(self, song: Song) -> bool:
        """Check if some playlist contains the specified song"""
        sql = "SELECT 1 FROM playlist_songs WHERE song_url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        return bool(cursor.fetchone())

    def filename_exists(self, filename: str) -> bool:
        """Check if some song uses the filename"""
        sql = "SELECT 1 FROM songs WHERE filename = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [filename])
        return bool(cursor.fetchone())

    def add_song(self, song: Song) -> None:
        """Add song to the database"""
        try:
            cursor = self._connection.cursor()
            sql = "INSERT INTO songs (url, uploader, yt_title, image_url, length) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(
                sql,
                [song.url, song.uploader, song.yt_title, song.image_url, song.length],
            )
            self._connection.commit()
        except sqlite3.IntegrityError:
            pass

    def set_song_as_downloaded(self, song: Song, filename: str) -> None:
        """Set song as downloaded and save the song filename to the database"""
        sql = "UPDATE songs SET downloaded = true, filename = ? WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [filename, song.url])
        self._connection.commit()

    def set_song_as_renamed(
        self, song: Song, artist: str, title: str, new_filename: str
    ) -> None:
        """Set song as renamed and save the title and the artist to the database"""
        sql = "UPDATE songs SET renamed = true, artist = ?, title = ?, filename = ? WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [artist, title, new_filename, song.url])
        self._connection.commit()

    def remove_song(self, song: Song) -> None:
        """Remove song from the database"""
        sql = "DELETE FROM songs WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        self._connection.commit()


song_repository = SongRepository()
