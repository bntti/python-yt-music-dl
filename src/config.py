import json
import os
import sys

file_dir = os.path.dirname(__file__)

config_file_path = f"{file_dir}/../config.json"
if not os.path.exists(config_file_path):
    sys.exit("Create config file to continue")  # TODO:

with open(config_file_path, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

SONG_EXT = ".mp3"
DATA_DIR = f"{file_dir}/../data"
SONG_DIR = f"{file_dir}/../songs"
DATABASE_FILE = f"{DATA_DIR}/database.sqlite"
