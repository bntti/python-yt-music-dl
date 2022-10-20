from colors import CLEAR, ITALIC, LINE, TITLE, WARN
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

MENU_STR = f"""{LINE}------------------------------{CLEAR}
{TITLE}What do you want to do?{CLEAR}
    {ITALIC}d{CLEAR} | download songs
    {ITALIC}r{CLEAR} | rename songs
    {ITALIC}u{CLEAR} | update cover images
    {ITALIC}e{CLEAR} | export renaming data
    {ITALIC}i{CLEAR} | import renaming data
    {ITALIC}q{CLEAR} | quit
{LINE}------------------------------{CLEAR}"""


def main() -> None:
    """Run the program"""
    initialize_database()

    while True:
        print(MENU_STR)
        command = input("Command: ").lower()
        if command == "d":
            check_playlists()
            download_songs()
            remove_orphans()
        elif command == "r":
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
            print(f"{WARN}Invalid command {ITALIC}{command}{CLEAR}")

        print()


if __name__ == "__main__":
    main()
