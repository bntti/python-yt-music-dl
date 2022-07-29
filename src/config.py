import json
import os
import sys

from colors import CLEAR, TITLE

file_dir = os.path.dirname(__file__)

config_file_path = f"{file_dir}/../config.json"
if not os.path.exists(config_file_path):
    with open(config_file_path, "w", encoding="utf-8") as f:
        f.write('{"DBFS": -20, "playlist_urls": []}')
    sys.exit(
        f"{TITLE}The configuration file was created, ",
        f"add the playlists there and rerun the program{CLEAR}",
    )

with open(config_file_path, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

SONG_EXT = ".mp3"
DATA_DIR = f"{file_dir}/../data"
SONG_DIR = f"{file_dir}/../songs"
DATABASE_FILE = f"{DATA_DIR}/database.sqlite"
