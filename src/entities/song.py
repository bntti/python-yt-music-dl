from typing import Optional


class Song:  # pylint: disable=[R0902]
    """Song object, matches a song on Youtube.

    Attributes:
        url (str): Song Youtube URL
        yt_title (str): Song title on Youtube
        length (int): Song length in seconds
        downloaded (bool): True if the song file is downloaded.
        filename (str): Song file filename.
        image_url (str): Url to the cover image of the song
        renamed (bool): True if the song has been renamed (artist and title have been set).
        title (str): Actual song title.
        artist (str): Song artist.
    """

    def __init__(  # pylint: disable=[R0913]
        self,
        url: str,
        uploader: str,
        yt_title: str,
        length: int,
        downloaded: bool = False,
        filename: Optional[str] = None,
        image_url: Optional[str] = None,
        renamed: bool = False,
        artist: Optional[str] = None,
        title: Optional[str] = None,
    ) -> None:
        """Constructor for a Song object

        Args:
            url (str): Song Youtube URL
            uploader (str): Song uploader on Youtube
            yt_title (str): Song title on Youtube
            length (int): Song length in seconds
            downloaded (bool, optional): True if the song file is downloaded. Defaults to False.
            filename (Optional[str], optional): Song file filename. Defaults to None.
            image_url (Optional[str], optional): Url to the cover image of the song
            renamed (bool, optional): True if the song has been
            renamed (artist and title have been set).
            artist (Optional[str], optional): Song artist. Defaults to None.
            title (Optional[str], optional): Actual song title. Defaults to None.
        """
        self.url = url
        self.uploader = uploader
        self.yt_title = yt_title
        self.length = length
        self.downloaded = downloaded
        self.filename = filename
        self.image_url = image_url
        self.renamed = renamed
        self.artist = artist
        self.title = title

    def __str__(self) -> str:
        if self.renamed:
            return f"{self.artist} - {self.title}"
        return f"{self.uploader}: {self.yt_title}"
