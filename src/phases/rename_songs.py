from repositories import song_repository
from services import song_renamer_service


def rename_songs():
    songs = song_repository.get_songs()
    print("Renaming songs")
    for i, song in enumerate(songs):
        if song.renamed:
            continue
        print(f"Renaming song {i+1}/{len(songs)}")
        print(song)

        artist = song.uploader
        title = song.yt_title
        if " - " in song.yt_title:
            artist, title = song.yt_title.split(" - ")[0:2]
        while True:
            input_artist = input(f"Song artist [{artist}]: ")
            input_title = input(f"Song title [{title}]: ")
            artist = input_artist if input_artist else artist
            title = input_title if input_title else title

            print(f"Artist: {artist}\nTitle: {title}")
            ok = input("OK? [Y/n]")
            if "n" not in ok.lower():
                break

        song_renamer_service.rename_song(song, artist, title)
