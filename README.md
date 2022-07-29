# PyYtMusic

A python app made with tkinter that downloads playlists from youtube and normalizes and plays the songs in them.  
Tests are currently a bit outdated.  

## Running project
### Dependencies
- ffmpeg
- poetry

### Commands
| Target                                     | Command                   |
| ------------------------------------------ | ------------------------- |
| Installing dependencies (excluding FFmpeg) | `poetry install`          |
| Running the program                        | `poetry run invoke start` |
| Running linting                            | `poetry run invoke lint`  |

### Configuration
Configuration is done by editing the `.env`  
All of the directories are created automatically
| Variable            | Default value     | Explanation                                                 |
| ------------------- | ----------------- | ----------------------------------------------------------- |
| `DATA_DIR_NAME`     | `data`            | Name of directory to save database and songs in             |
| `SONG_DIR_NAME`     | `songs`           | Name of directory for songs (will be under `DATA_DIR_NAME`) |
| `DATABASE_FILENAME` | `database.sqlite` | Name of database file (will be under `DATA_DIR_NAME`)       |
| `TARGET_DBFS`       | `-20`             | Target dBFS to normalize songs to                           |
