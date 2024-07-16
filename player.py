import time
from typing import List

import vlc
import os

from general import get_extension_callable, PlaylistRecord

os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

stations_list = [
    "http://nl.ah.fm:8000/live",  # A pretty one
    "http://streams.echoesofbluemars.org:8000/bluemars"
]


class InternetPlayer:
    _instance: vlc.Instance
    _player: vlc.MediaPlayer

    def __init__(self):
        self._instance = vlc.Instance()
        self._player = self._instance.media_player_new()

    def set_web_station(self, station_name: str) -> None:
        media = self._instance.media_new(station_name)
        self._player.set_media(media)
        self._player.play()
        try:
            time.sleep(2)
            print("Плеер начал воспроизведение. Нажмите Ctrl+C для остановки.")
            while True:
                state = self._player.get_state()
                if state not in [vlc.State.Playing, vlc.State.Buffering]:
                    print("Воспроизведение остановлено или возникла ошибка.")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print("Воспроизведение остановлено пользователем.")

    @staticmethod
    def get_playlist(playlist_path: str) -> List[PlaylistRecord]:
        playlist_function = get_extension_callable(playlist_path)
        return playlist_function(playlist_path)


def test_get_web_stations_from_m3u(m3u_path: str):
    player = InternetPlayer()
    playlist = player.get_playlist(m3u_path)
    for record in playlist:
        print(record.__dict__)


def test_set_web_station(station: str):
    player = InternetPlayer()
    player.set_web_station(station)


test_get_web_stations_from_m3u("test.pls")
# test_set_web_station("https://e20.yesstreaming.net:8279")
