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
        cursor.execute("SELECT url, title, image_url FROM playlists")
        rows = cursor.fetchall()

        playlists = []
        for row in rows:
            songs = song_repository.get_playlist_songs(row["url"])
            playlist = Playlist(row["url"], row["title"], row["image_url"], songs)
            playlists.append(playlist)
        return playlists

    def get_playlist(self, url: str) -> Playlist:
        """Fetches the playlist with the corresponding url. Returns None if one doesn't exist"""
        cursor = self._connection.cursor()
        sql = "SELECT url, title, image_url FROM playlists WHERE url = ?"
        cursor.execute(sql, [url])
        row = cursor.fetchone()

        if not row:
            raise Exception(f"Tried to get playlist that does not exist (URL: {url})")

        songs = song_repository.get_playlist_songs(row["url"])
        return Playlist(row["url"], row["title"], row["image_url"], songs)

    def get_song_playlist(self, song: Song) -> Playlist:
        """Get the playlist that the song is in"""
        sql = """SELECT p.url, p.title, p.image_url
                 FROM playlists p, songs s
                 WHERE s.playlist_url = p.url AND s.url = ?"""
        cursor = self._connection.cursor()
        cursor.execute(sql, [song.url])
        row = cursor.fetchone()

        if not row:
            raise Exception(
                f"Tried to get playlist for song that does not have a playlist (song: {song})"
            )

        return Playlist(
            row["url"],
            row["title"],
            row["image_url"],
            song_repository.get_playlist_songs(row["url"]),
        )

    def playlist_exists(self, playlist: Playlist) -> bool:
        """Check if a playlist with the specified url is in the database"""
        sql = "SELECT 1 FROM playlists WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist.url])
        return bool(cursor.fetchone())

    def add_playlist(self, playlist: Playlist) -> None:
        """Add a playlist to the database"""
        sql = "INSERT INTO playlists (url, title, image_url) VALUES (?, ?, ?)"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist.url, playlist.title, playlist.image_url])
        self._connection.commit()

        for song in playlist:
            if song_repository.song_exists(song.url):
                song_repository.update_song_playlist(playlist, song)
            else:
                song_repository.add_song(playlist, song)

    def remove_playlist(self, playlist: Playlist) -> None:
        """Removes a playlist from the database"""
        sql = "DELETE FROM playlists WHERE url = ?"
        cursor = self._connection.cursor()
        cursor.execute(sql, [playlist.url])
        self._connection.commit()


playlist_repository = PlaylistRepository()
