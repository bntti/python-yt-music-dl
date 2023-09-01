import copy
import os
import shutil
import sys
from io import BytesIO

import pydub
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3._frames import APIC
from mutagen.mp3 import MP3
from pathvalidate import sanitize_filepath
from PIL import Image, ImageFilter

from config import CONFIG, SONG_DIR, SONG_EXT
from entities import Playlist, Song
from repositories import playlist_repository, song_repository


def sanitize_filename(original_filename: str) -> str:
    """Sanitize filename"""
    sanitized_filename = str(sanitize_filepath(original_filename))
    sanitized_filename = sanitized_filename.replace("/", " ")

    return sanitized_filename


def get_song_filename(
    old_filename: str | None, artist: str, title: str, assert_unique: bool = False
) -> str:
    """Get sanitized filename for song"""
    filename = sanitize_filename(f"{artist} - {title}")

    if (
        old_filename != filename
        and assert_unique
        and song_repository.filename_exists(filename)
    ):
        sys.exit(f"Filename exists '{filename}'")

    return filename


def create_playlist_folder(filename: str) -> None:
    """Create folder (for playlist) if necessary"""
    path = os.path.join(SONG_DIR, filename)
    if not os.path.exists(path):
        os.mkdir(path)


def get_song_path(song: Song) -> str:
    """Get path of song file"""
    if song.folder is None or song.filename is None:
        raise Exception(f"Tried to get path to song {song} with no folder/filename")
    return os.path.join(SONG_DIR, song.folder, song.filename + SONG_EXT)


def rename_song(song: Song, new_filename: str) -> None:
    """Rename song to new filename"""
    song_copy = copy.deepcopy(song)
    old_path = get_song_path(song_copy)
    song_copy.filename = new_filename
    new_path = get_song_path(song_copy)
    shutil.move(old_path, new_path)


def generate_square_image(image: Image.Image) -> Image.Image:
    """Convert image to 1:1 by adding blur"""
    original_w, original_h = image.size
    factor = max(original_w, original_h) / min(original_w, original_h)
    new_w = int(original_w * factor)
    new_h = int(original_h * factor)
    background = image.resize((new_w, new_h))
    background = background.filter(ImageFilter.GaussianBlur(11))

    target_bg_size = min(new_w, new_h)
    x_offset = int((new_w - target_bg_size) / 2)
    y_offset = int((new_h - target_bg_size) / 2)
    background = background.crop(
        (x_offset, y_offset, new_w - x_offset, new_h - y_offset)
    )

    x_offset = int((target_bg_size - original_w) / 2)
    y_offset = int((target_bg_size - original_h) / 2)
    background.paste(image, (x_offset, y_offset))
    return background


def get_song_cover_image(image_url: str) -> bytes:
    """Generate cover image from image url"""
    data = requests.get(image_url, timeout=10).content
    image = Image.open(BytesIO(data))
    original_w, original_h = image.size

    if original_w == original_h:
        square_image = image
    else:
        square_image = generate_square_image(image)

    buf = BytesIO()
    square_image.save(buf, format="png")
    return buf.getvalue()


def write_cover_images(playlist: Playlist) -> None:
    """Write/update song cover images"""
    image_data = get_song_cover_image(playlist.image_url)

    for song in playlist:
        if song.image_url == playlist.image_url:
            continue

        mp3_file = MP3(get_song_path(song))
        mp3_file.tags.add(  # type: ignore
            APIC(
                encoding=3,
                mime="image/png",
                type=3,
                desc="Cover",
                data=image_data,
            )
        )
        mp3_file.save()
        song_repository.update_song_image_url(song, playlist.image_url)


def write_song_metadata(song: Song, playlist: Playlist) -> None:
    """Write the song metadata"""
    mp3_file = MP3(get_song_path(song), ID3=EasyID3)
    mp3_file["album"] = [playlist.title]

    artist = song.uploader
    title = song.yt_title
    if " - " in song.yt_title:
        artist, title = song.yt_title.split(" - ")[0:2]
    mp3_file["artist"] = [artist]
    mp3_file["title"] = [title]
    mp3_file.save()


def update_song_metadata(
    song: Song, artist: str, title: str, new_filename: str
) -> None:
    """Write the new artist and the new title to the song metadata"""
    song_copy = copy.deepcopy(song)
    song_copy.filename = new_filename
    mp3_file = MP3(get_song_path(song_copy), ID3=EasyID3)
    mp3_file["artist"] = [artist]
    mp3_file["title"] = [title]
    mp3_file.save()


def normalize_and_convert_song_to_the_correct_format(song_path: str) -> str:
    """Normalize song, convert song file to configured format and return the filename"""
    base_path, filename = os.path.split(song_path)
    filename, ext = os.path.splitext(filename)
    new_path = os.path.join(base_path, filename + SONG_EXT)

    song_audio = pydub.AudioSegment.from_file(song_path, format=ext[1:])
    loudness_difference = CONFIG["DBFS"] - song_audio.dBFS
    normalized = song_audio.apply_gain(loudness_difference)
    normalized.export(new_path, format=SONG_EXT[1:])
    os.remove(song_path)

    return filename


def delete_folder(path: str) -> None:
    """Delete all files in the folder and then the folder itself"""
    files = os.listdir(path)
    for file in files:
        os.remove(os.path.join(path, file))
    os.rmdir(path)


def remove_extra_song_folders() -> None:
    """Remove empty directories from SONG_DIR"""
    folders = os.listdir(SONG_DIR)
    for folder in folders:
        if not playlist_repository.filename_exists(folder):
            delete_folder(os.path.join(SONG_DIR, folder))


def delete_song_file(song: Song) -> None:
    """Delete song file"""
    os.remove(get_song_path(song))
