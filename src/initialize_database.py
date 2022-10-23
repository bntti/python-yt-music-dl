from sqlite3 import Connection

from database_connection import get_database_connection


def create_tables(connection: Connection) -> None:
    """Create all tables"""
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE playlists (
            url       TEXT NOT NULL PRIMARY KEY,
            title     TEXT NOT NULL,
            image_url TEXT NOT NULL
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE songs (
            url          TEXT NOT NULL PRIMARY KEY,
            yt_title     TEXT NOT NULL,
            uploader     TEXT NOT NULL,
            length       INT  NOT NULL,
            playlist_url TEXT,
            downloaded   BOOL NOT NULL DEFAULT false,
            filename     TEXT,
            image_url    TEXT,
            renamed      bool NOT NULL DEFAULT false,
            artist       TEXT,
            title        TEXT,
            FOREIGN KEY (playlist_url) REFERENCES playlists(url) ON DELETE SET NULL
        );
        """
    )

    connection.commit()


def initialize_database() -> None:
    """Create the database tables if necessary"""
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
    result = cursor.fetchone()[0]
    if result == 0:
        create_tables(connection)
