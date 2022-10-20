import json
import os

from colors import CLEAR, INFO, ITALIC, TITLE
from repositories import song_repository


def export_data() -> None:
    """Export song renaming data to ../../export.json"""
    print(f"{TITLE}Exporting renaming data{CLEAR}")
    data = song_repository.export()
    file_dir = os.path.dirname(__file__)
    file_path = f"{file_dir}/../../export.json"
    with open(file_path, "w", encoding="utf-8") as export_file:
        json.dump(data, export_file)
    print(f"{INFO}Exported data was written to {ITALIC}{file_path}{CLEAR}")
