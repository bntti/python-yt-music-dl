from typing import Dict, List, Tuple

from database_connection import get_database_connection
from entities import Playlist, Song


class SongRepository:
    """Handles saving song objects to the database"""

    def __init__(self) -> None:
        self._connection = get_database_connection()

    @staticmethod
    def row_to_song(row: dict) -> Song:
        """Convert a SQL row object to a Song object"""
        return Song(
            row["url"],
            row["uploader"],
            row["yt_title"],
            row["length"],
            row["downloaded"],
            row["folder"],
            row["filename"],
            row["image_url"],
            row["renamed"],
            row["artist"],
            row["title"],
        )

    def get_songs(self) -> List[Song]:
        """Fetches a list of all the songs in the database"""
        sql = "SELECT * FROM songs WHERE playlist_url IS NOT NULL"
        cursor = self._connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [self.row_to_song(row) for row in rows]

    def get_orphans(self) -> List[Song]:
        """Fetches a list of all the songs in the database"""
        sql = "SELECT * FROM songs WHERE playlist_url IS NULL"
        cursor = self._connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [self.row_to_song(row) for row in rows]

    def get_song(self, song_url: str) -> Song:
        """Fetches a song with the corresponding URL and returns None if one does not exist"""
        sql = "SELECT * FROM songs WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [song_url])
        row = cursor.fetchone()

        if not row:
            raise Exception(f"No song in the database with url {song_url}")

        return self.row_to_song(row)

    def get_nums(self) -> Tuple[int, int]:
        """Return the number of (undownloaded, unrenamed, orhphaned) songs"""
        cursor = self._connection.cursor()

        sql = "SELECT COUNT(*) FROM songs WHERE downloaded = true"
        cursor.execute(sql)
        downloaded = int(cursor.fetchone()[0])

        sql = "SELECT COUNT(*) FROM songs WHERE downloaded = true and renamed = false"
        cursor.execute(sql)
        renamed = int(cursor.fetchone()[0])

        return (downloaded, renamed)

    def add_song(self, playlist: Playlist, song: Song) -> None:
        """Add song to the database"""
        if self.song_exists(song.url):
            raise Exception("Tried to add song that already exists")

        cursor = self._connection.cursor()
        sql = """INSERT INTO songs (url, uploader, yt_title, length, playlist_url, folder)
                VALUES (?, ?, ?, ?, ?, ?)"""
        cursor.execute(
            sql,
            [
                song.url,
                song.uploader,
                song.yt_title,
                song.length,
                playlist.url,
                playlist.filename,
            ],
        )
        self._connection.commit()

    def song_has_playlist(self, song: Song) -> bool:
        """Return true if the song is in some plalylist"""
        sql = "SELECT 1 FROM songs WHERE url = ? AND playlist_url IS NOT NULL"
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        return bool(cursor.fetchone())

    def get_playlist_songs(self, playlist_url: str) -> List[Song]:
        """Fetches the list of songs that are in the specified playlist"""
        sql = "SELECT * FROM songs WHERE playlist_url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist_url])
        rows = cursor.fetchall()
        return [self.row_to_song(row) for row in rows]

    def filename_exists(self, filename: str) -> bool:
        """Check if some other song uses the filename"""
        sql = "SELECT 1 FROM songs WHERE filename = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [filename])
        return bool(cursor.fetchone())

    def song_exists(self, song_url: str) -> bool:
        """Check if the song is in the database"""
        sql = "SELECT 1 FROM songs WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [song_url])
        return bool(cursor.fetchone())

    def set_song_as_downloaded(self, song: Song, filename: str) -> None:
        """Set song as downloaded and save the song filename to the database"""
        sql = "UPDATE songs SET downloaded = true, filename = ? WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [filename, song.url])
        self._connection.commit()

    def update_song_image_url(self, song: Song, image_url: str) -> None:
        """Set song as downloaded and save the song filename to the database"""
        sql = "UPDATE songs SET image_url = ? WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [image_url, song.url])
        self._connection.commit()

    def set_song_as_renamed(
        self, song: Song, artist: str, title: str, new_filename: str
    ) -> None:
        """Set song as renamed and save the title and the artist to the database"""
        sql = "UPDATE songs SET renamed = true, artist = ?, title = ?, filename = ? WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [artist, title, new_filename, song.url])
        self._connection.commit()

    def export(self) -> List[Dict]:
        """Export renamed song urls, artists and titles"""
        cursor = self._connection.cursor()
        cursor.execute("SELECT url, artist, title FROM songs WHERE renamed = true")
        rows = cursor.fetchall()
        return [
            {"url": row["url"], "artist": row["artist"], "title": row["title"]}
            for row in rows
        ]

    def update_song_playlist(self, song: Song, new_playlist: Playlist) -> None:
        """Update song playlist"""
        if self.song_has_playlist(song):
            raise Exception(
                "Song {song} was being added to new playlist even though it was already in one"
            )

        sql = "UPDATE songs SET playlist_url = ?, folder = ? WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [new_playlist.url, new_playlist.filename, song.url])
        self._connection.commit()

    def get_song_playlist_url(self, song: Song) -> str:
        """Get song playlist url"""
        sql = "SELECT playlist_url FROM songs WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        playlist_url = cursor.fetchone()
        if not playlist_url:
            raise Exception("Tried to get song playlist url but the url is Null")
        return cursor.fetchone()

    def remove_song_from_playlist(self, song: Song) -> None:
        """Removes a playlist from the playlist"""
        sql = "UPDATE songs SET playlist_url = NULL WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        self._connection.commit()

    def remove_song(self, song: Song) -> None:
        """Remove song from the database"""
        sql = "DELETE FROM songs WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        self._connection.commit()


song_repository = SongRepository()
