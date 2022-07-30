import json
import os
import sys

from colors import CLEAR, ERROR, ITALIC, SUBTITLE, TITLE
from repositories import song_repository
from services import song_renamer_service


def import_data():
    print(f"{TITLE}Importing song renaming data{CLEAR}")
    file_dir = os.path.dirname(__file__)
    file_path = f"{file_dir}/../../export.json"
    if not os.path.exists(file_path):
        sys.exit(f"{ERROR}File {ITALIC}{file_path}{ERROR} does not exist")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"{TITLE}Renaming songs{CLEAR}")
    for i, song_data in enumerate(data):
        song = song_repository.get_song(song_data["url"])
        if song is not None:
            print(f"{SUBTITLE}Renaming song {i+1}/{len(data)}{CLEAR}")
            song_renamer_service.rename_song(
                song, song_data["artist"], song_data["title"]
            )
