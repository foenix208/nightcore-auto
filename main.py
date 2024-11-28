import requests
from bs4 import BeautifulSoup
import random 

from pytubefix import Playlist
from pytubefix.cli import on_progress

import random
import os 

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip, concatenate_audioclips


def wallpaper_url(url_tags):
    r = requests.get(url_tags)
    temps = []
    if r.ok:
        soup = BeautifulSoup(r.text,"lxml")
        soup = soup.find_all("a",{"class":"g1-frame"})

        for i in soup:
            temps.append(i["href"])

        return temps
    
def wallpaper(url):
    r = requests.get(url)
    if r.ok:
        soup = BeautifulSoup(r.text,"lxml")
        soup = soup.find_all("source")

        print(soup[len(soup)-1]["src"])
        return soup[len(soup)-1]["src"]
    
    else:
        print("[ X ] Erreur")

def wallpaper_dlw(url, chemin_de_telechargement):

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(chemin_de_telechargement, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"La vidéo a été téléchargée avec succès dans {chemin_de_telechargement}")

        else:
            print(f"Impossible de télécharger la vidéo, code de statut : {response.status_code}")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")

def musique_dlw(url):
    pl = Playlist(url)

    for i in range(20):
        pl.videos[random.randint(0,len(pl)-1)].streams.get_audio_only().download(output_path="resources/music/")

def create_video():
    temp = 0

    toto = os.listdir("./resources/music/")
    audio_paths = []

    for i in toto:
        audio_paths.append(f"./resources/music/{i}")

    # Chemins vers les fichiers
    video_path = "./resources/wallpaper/video.mp4"

    # Charger la vidéo et créer une boucle
    background_video = VideoFileClip(video_path)
    video_duration = sum(AudioFileClip(audio).duration for audio in audio_paths)  # Durée totale des pistes audio
    looped_video = concatenate_videoclips([background_video] * int(video_duration // background_video.duration + 1)).subclip(0, video_duration)

    # Charger et combiner les pistes audio
    audio_clips = [AudioFileClip(audio) for audio in audio_paths]
    combined_audio = concatenate_audioclips(audio_clips)

    # Ajouter l'audio combiné à la vidéo
    final_video = looped_video.set_audio(combined_audio)

    # Sauvegarder la vidéo finale
    output_path = "final_video.mp4"
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    print(f"Vidéo finale créée avec succès : {output_path}")

wallpaper_dlw(wallpaper(wallpaper_url("https://moewalls.com/category/anime/page/1/?order=newest")[random.randint(0,10)]),"./resources/wallpaper/video.mp4")
musique_dlw("https://www.youtube.com/playlist?list=PL6Go6XFhidEBmeOa3v_m0_287za6afK-C")
    
create_video()