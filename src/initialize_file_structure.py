import os

import config


def init_file_structure() -> None:
    """Create the data folder and the song folder"""
    dirs = [config.DATA_DIR, config.SONG_DIR]
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
