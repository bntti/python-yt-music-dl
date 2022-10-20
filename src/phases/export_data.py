import json
import os

import custom_io as io
from repositories import song_repository


def export_data() -> None:
    """Export song renaming data to ../../export.json"""
    io.title("Exporting renaming data")
    data = song_repository.export()
    file_dir = os.path.dirname(__file__)
    file_path = f"{file_dir}/../../export.json"
    with open(file_path, "w", encoding="utf-8") as export_file:
        json.dump(data, export_file)
    io.info("Exported data was written to %s", file_path)
