import json
import os

import custom_io as io
from repositories import file_repository, song_repository
from services import song_service


def import_data() -> None:
    """Import song renaming data from ../../export.json and rename songs according to it"""
    io.title("Importing song renaming data")
    file_dir = os.path.dirname(__file__)
    file_path = f"{file_dir}/../../export.json"
    if not os.path.exists(file_path):
        io.error("File %s does not exist", file_path)
        return

    with open(file_path, "r", encoding="utf-8") as data_file:
        data = json.load(data_file)

    io.title("Renaming songs")
    for song_data in data:
        if not song_repository.song_exists(song_data["url"]):
            continue

        song = song_repository.get_song(song_data["url"])
        old_filename = song.filename
        new_filename = file_repository.get_song_filename(
            old_filename, song_data["artist"], song_data["title"], False
        )
        if (
            song.artist != song_data["artist"]
            or song.title != song_data["title"]
            or song.filename != new_filename
        ):
            print(f"Old filename: {song.filename}\nNew filename: {new_filename}\n")
            song_service.rename_song(song, song_data["artist"], song_data["title"])
