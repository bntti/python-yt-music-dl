import json
import os

from colors import CLEAR, INFO, ITALIC, TITLE
from repositories import song_repository


def export_data():
    print(f"{TITLE}Exporting renaming data{CLEAR}")
    data = song_repository.export()
    file_dir = os.path.dirname(__file__)
    file_path = f"{file_dir}/../../export.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"{INFO}Exported data was written to {ITALIC}{file_path}{CLEAR}")
