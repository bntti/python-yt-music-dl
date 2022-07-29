import copy
import os
import shutil
from io import BytesIO

import pydub
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC
from mutagen.mp3 import MP3
from PIL import Image, ImageFilter

from config import CONFIG, SONG_DIR, SONG_EXT
from entities import Playlist, Song


class FileRepository:
    """Manages files, preferably all file operations would be done using this repository"""

    @staticmethod
    def get_song_path(song: Song) -> str:
        """Get path of song file"""
        return os.path.join(SONG_DIR, song.filename + SONG_EXT)

    def rename_song(self, song: Song, new_filename: str) -> None:
        """Rename song to new filename"""
        song_copy = copy.deepcopy(song)
        old_path = self.get_song_path(song_copy)
        song_copy.filename = new_filename
        new_path = self.get_song_path(song_copy)
        shutil.move(old_path, new_path)

    def generate_square_image(self, image: Image) -> Image:
        """Convert image to 1:1 by adding blur"""
        original_w, original_h = image.size
        factor = max(original_w, original_h) / min(original_w, original_h)
        new_w = int(original_w * factor)
        new_h = int(original_h * factor)
        background = image.resize((new_w, new_h))
        background = background.filter(ImageFilter.GaussianBlur(7))

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

    def get_song_cover_image(self, image_url: str) -> bytes:
        """Generate cover image from image url"""
        data = requests.get(image_url).content
        image = Image.open(BytesIO(data))
        original_w, original_h = image.size

        if original_w == original_h:
            square_image = image
        else:
            square_image = self.generate_square_image(image)

        buf = BytesIO()
        square_image.save(buf, format="png")
        return buf.getvalue()

    def check_song_album(self, song: Song, playlist: Playlist):
        """Check song album and set it if necessary"""
        mp3_file = MP3(self.get_song_path(song), ID3=EasyID3)
        if "album" not in mp3_file or mp3_file["album"] != [playlist.title]:
            mp3_file["album"] = [playlist.title]
            mp3_file.save()

            mp3_file = MP3(self.get_song_path(song))
            mp3_file.tags.add(
                APIC(
                    encoding=3,
                    mime="image/png",
                    type=3,
                    desc="Cover",
                    data=self.get_song_cover_image(playlist.image_url),
                )
            )
            mp3_file.save()

    def write_song_tags(
        self, song: Song, artist: str, title: str, new_filename: str
    ) -> None:
        """Write song tags to the song file"""
        song_copy = copy.deepcopy(song)
        song_copy.filename = new_filename
        mp3_file = MP3(self.get_song_path(song_copy), ID3=EasyID3)
        mp3_file["artist"] = [artist]
        mp3_file["title"] = [title]
        mp3_file.save()

    @staticmethod
    def normalize_and_convert_song_to_the_correct_format(path: str) -> str:
        """Normalize song, convert song file to configured format and return the filename"""
        base, ext = os.path.splitext(path)
        filename = os.path.basename(base)
        new_path = os.path.join(SONG_DIR, filename + SONG_EXT)

        song_audio = pydub.AudioSegment.from_file(path, format=ext[1:])
        loudness_difference = CONFIG["DBFS"] - song_audio.dBFS
        normalized = song_audio.apply_gain(loudness_difference)
        normalized.export(new_path, format=SONG_EXT[1:])
        os.remove(path)

        return filename

    def delete_song_file(self, song: Song) -> None:
        """Delete song file"""
        os.remove(self.get_song_path(song))


file_repository = FileRepository()
