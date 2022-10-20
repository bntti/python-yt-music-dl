from sqlite3 import Connection

from database_connection import get_database_connection


def drop_tables(connection: Connection) -> None:
    """Drop all tables"""
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS playlist_songs")
    cursor.execute("DROP TABLE IF EXISTS playlists")
    cursor.execute("DROP TABLE IF EXISTS songs")

    connection.commit()


def create_tables(connection: Connection) -> None:
    """Create all tables"""
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE playlists (
            url       TEXT NOT NULL PRIMARY KEY,
            title     TEXT NOT NULL,
            image_url TEXT NOT NULL,
            is_album  BOOL NOT NULL
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE playlist_songs (
            playlist_url TEXT NOT NULL,
            song_url     TEXT NOT NULL,
            FOREIGN KEY (playlist_url) REFERENCES playlists(url) ON DELETE CASCADE,
            FOREIGN KEY (song_url)     REFERENCES songs(url)     ON DELETE CASCADE,
            PRIMARY KEY (playlist_url, song_url)
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE songs (
            url        TEXT NOT NULL PRIMARY KEY,
            yt_title   TEXT NOT NULL,
            uploader   TEXT NOT NULL,
            length     INT  NOT NULL,
            downloaded BOOL NOT NULL DEFAULT false,
            filename   TEXT,
            image_url  TEXT,
            renamed    bool NOT NULL DEFAULT false,
            artist     TEXT,
            title      TEXT
        );
        """
    )

    connection.commit()


def clear_tables() -> None:
    """Delete all data from the database"""
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM playlists")
    cursor.execute("DELETE FROM songs")
    cursor.execute("DELETE FROM playlist_songs")
    connection.commit()


def reset_database() -> None:
    """Drop all tables and recreate them"""
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)


def initialize_database() -> None:
    """Create the database tables if necessary"""
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
    result = cursor.fetchone()[0]
    if result == 0:
        reset_database()
