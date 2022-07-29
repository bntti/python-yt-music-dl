# yt-music-dl

Downloads songs from youtube, renames them and writes the song metadata

## Running project
### Dependencies
- ffmpeg
- poetry

### Commands
| Target                  | Command                   |
| ----------------------- | ------------------------- |
| Installing dependencies | `poetry install`          |
| Running the program     | `poetry run invoke start` |
| Running linting         | `poetry run invoke lint`  |

### Configuration
The program is configured by editing `config.json`. If the file does not exist, run the program once.
| Variable        | Default value | Explanation                       |
| --------------- | ------------- | --------------------------------- |
| `DBFS`          | `-20`         | Target dBFS to normalize songs to |
| `playlist_urls` | `[]`          | List of the URLs of the playlists |
