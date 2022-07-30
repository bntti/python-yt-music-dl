# yt-music-dl

Downloads playlists from youtube, writes the song metadata and allows the user to manually input the song artists/titles.  
One song can only be in one playlist, with the exception of a song being in an album and a playlist, where the album is given priority.  

Metadata written:
- `album`, playlist title
- `cover image`, playlist thumbnail
- `artist`, the program tries to guess the song artist but the user can input the correct one 
- `title`, the program tries to guess the song title but the user can input the correct one 

## Running project
### Dependencies
- ffmpeg
- poetry

### Installing dependencies
```
poetry install
```

### Running the program
```
poetry run invoke start
```

### Usage
| Command                         | Description                                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------------------- |
| _`d`_` \| download songs`       | Check the playlists for changes and download the new songs                                  |
| _`r`_` \| rename songs`         | Rename songs that have not been renamed yet                                                 |
| _`e`_` \| export renaming data` | Export the user inputted artist-title pairs to `export.json`                                |
| _`i`_` \| import renaming data` | Import the user inputted artist-title pairs from a `export.json` file in this projects root |
| _`q`_` \| quit`                 | Exit the program                                                                            |

### Configuration
The program is configured by editing `config.json`. This file is generated when you run the program for the first time.
| Variable        | Default value | Explanation                       |
| --------------- | ------------- | --------------------------------- |
| `DBFS`          | `-20`         | Target dBFS to normalize songs to |
| `playlist_urls` | `[]`          | List of the URLs of the playlists |
