import json
import os
import sys

from colors import CLEAR, ERROR, ITALIC, SUBTITLE, TITLE
from repositories import song_repository
from services import song_renamer_service


def import_data() -> None:
    """Import song renaming data from ../../export.json and rename songs according to it"""
    print(f"{TITLE}Importing song renaming data{CLEAR}")
    file_dir = os.path.dirname(__file__)
    file_path = f"{file_dir}/../../export.json"
    if not os.path.exists(file_path):
        sys.exit(f"{ERROR}File {ITALIC}{file_path}{ERROR} does not exist")

    with open(file_path, "r", encoding="utf-8") as data_file:
        data = json.load(data_file)

    print(f"{TITLE}Renaming songs{CLEAR}")
    for i, song_data in enumerate(data):
        song = song_repository.get_song(song_data["url"])
        if song is not None:
            song_renamer_service.rename_song(
                song, song_data["artist"], song_data["title"]
            )
