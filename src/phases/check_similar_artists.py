from difflib import get_close_matches

from repositories import song_repository


def check_similar_artists():
    songs = song_repository.get_songs()
    artists = []
    for song in songs:
        assert song.artist
        if song.artist not in artists:
            artists.append(song.artist)

    for song in songs:
        assert song.artist
        matches = get_close_matches(song.artist, artists, cutoff=0.7)
        if len(matches) > 1:
            print(song, matches)
