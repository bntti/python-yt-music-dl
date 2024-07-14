# yt-music-dl

**Archived**

See updated version at [yt-music-dl](https://github.com/bntti/yt-music-dl), written with typescript.

---

Downloads playlists from youtube, writes the song metadata and allows the user to manually input the song artists/titles. One song can only be in one playlist.

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

| Command                            | Description                                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| `d \| download songs`              | Check the playlists for changes and download the new songs                                  |
| `r \| rename songs`                | Rename songs that have not been renamed yet                                                 |
| `e \| export renaming data`        | Export the user inputted artist-title pairs to `export.json`                                |
| `c \| check for duplicate artists` | Prints artists that are similar to each other to check for typos                            |
| `i \| import renaming data`        | Import the user inputted artist-title pairs from a `export.json` file in this projects root |
| `q \| quit`                        | Exit the program                                                                            |

### Configuration

The program is configured by editing `config.json`. This file is generated when you run the program for the first time.

| Variable        | Default value | Explanation                       |
| --------------- | ------------- | --------------------------------- |
| `DBFS`          | `-20`         | Target dBFS to normalize songs to |
| `playlist_urls` | `[]`          | List of the URLs of the playlists |
