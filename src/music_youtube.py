from pytubefix import YouTube
from pytubefix.cli import on_progress

from pytubefix import Playlist
from pytubefix.cli import on_progress

import random


def ft_musique(file="./",time="60",data = None):
    url = "https://www.youtube.com/playlist?list=PL3-sRm8xAzY-w9GS19pLXMyFRTuJcuUjy"

    pl = Playlist(url)
    Playlists = []

    for video in pl.videos:
        Playlists.append(video.streams.get_audio_only())



    for _ in range(10):
        y = random.choice(Playlists)
        print(y.title)
        y.download(output_path=file)