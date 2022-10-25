import custom_io as io
from custom_io import CLEAR, LINE, OPTION, TITLE
from initialize_database import initialize_database
from phases import (
    check_playlists,
    download_songs,
    export_data,
    import_data,
    remove_orphans,
    rename_songs,
    update_cover_images,
)
from repositories import song_repository

MENU_STR = f"""{LINE}------------------------------{CLEAR}
{OPTION}Number of songs to download{CLEAR} | %s
{OPTION}Number of songs to rename{CLEAR}   | %s
{OPTION}Number of orhphaned songs{CLEAR}   | %s

{TITLE}What do you want to do?{CLEAR}
    {OPTION}r{CLEAR} | refresh playlists
    {OPTION}d{CLEAR} | download songs
    {OPTION}n{CLEAR} | rename songs
    {OPTION}u{CLEAR} | update cover images
    {OPTION}e{CLEAR} | export renaming data
    {OPTION}i{CLEAR} | import renaming data
    {OPTION}q{CLEAR} | quit
{LINE}------------------------------{CLEAR}"""


def main() -> None:
    """Run the program"""
    initialize_database()

    while True:
        print(MENU_STR % song_repository.get_nums())
        try:
            command = input("Command: ").lower()
        except EOFError:
            command = "q"

        if command == "r":
            check_playlists()
        elif command == "d":
            download_songs()
            remove_orphans()
        elif command == "n":
            rename_songs()
        elif command == "u":
            update_cover_images()
        elif command == "e":
            export_data()
        elif command == "i":
            import_data()
        elif command in ("q", ""):
            break
        else:
            io.warn("Invalid command %s", command)

        print()


if __name__ == "__main__":
    main()
