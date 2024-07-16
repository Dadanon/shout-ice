# Shoutcast Icecast Player (ShIP)

Класс, тестирующий возможность проигрывания радиостанций
по протоколам Shoutcast и Icecast с помощью vlc

Инициализация плеера
```
player = InternetPlayer()
```
На данный момент (16.07.24) доступны следующие методы
### 1. Установить станцию и начать проигрывание
```
set_web_station(station_name: str) -> None
```
Тестовый метод для проверки воспроизведения онлайн станций с помощью vlc
### 2. Получить список позиций для воспроизведения
```
get_playlist(playlist_path: str) -> List[PlaylistRecord]
```
```
class PlaylistRecord:
    url: str
    duration: Optional[float]
    name: Optional[str]
```
Получает список объектов указанного типа. На данный момент (16.07.24)
поддерживает форматы .m3u, .m3u8, .pls.  
Пример получения данных:
```
player = InternetPlayer()
playlist = player.get_playlist('test.pls')
for record in playlist:
    print(record.__dict__)
```
Вывод:
```
{'url': 'https://e20.yesstreaming.net:8279/', 'duration': -1.0, 'name': None}
{'url': 'example2.mp3', 'duration': 120.0, 'name': 'Just some local audio that is 2mins long'}
{'url': 'F:\\Music\\whatever.m4a', 'duration': None, 'name': 'absolute path on Windows'}
{'url': '%UserProfile%\\Music\\short.ogg', 'duration': 5.0, 'name': 'example for an Environment variable'}
```
Длительность (duration) указывается в секундах, непонятно насколько точно. Длительность равная -1.0
означает, что ссылка (url) указывает на потоковое аудио.