from initialize_database import initialize_database
from phases import check_playlists, download_songs, remove_orphans, rename_songs


def main() -> None:
    """Run the program"""
    initialize_database()

    check_playlists()
    download_songs()
    rename_songs()
    remove_orphans()


if __name__ == "__main__":
    main()
