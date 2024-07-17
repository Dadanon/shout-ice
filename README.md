# Shoutcast Icecast Player (ShIP)

Класс, тестирующий возможность проигрывания радиостанций
по протоколам Shoutcast и Icecast с помощью vlc. Также позволяет 
получать список новостных лент и подкастов из .opml файлов

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
get_playlist(playlist_path: str) -> List[PlaylistRecord | OPMLRecord]
```
```
class PlaylistRecord:
    url: str
    duration: Optional[float]
    name: Optional[str]
```
```
class OPMLRecord:
    type: str
    text: str
    xml_url: str
    description: Optional[str]
    html_url: Optional[str]
    language: Optional[str]
    title: Optional[str]
    version: Optional[str]
```
Получает список объектов указанного типа. На данный момент (16.07.24)
поддерживает форматы .m3u, .m3u8, .pls., .opml  
Пример получения данных:
```
player = InternetPlayer()
playlist = player.get_playlist('test.pls')
for record in playlist:
    print(record.__dict__)
```
Вывод: (.m3u, .m3u8, .pls)
```
{'url': 'https://e20.yesstreaming.net:8279/', 'duration': -1.0, 'name': None}
{'url': 'example2.mp3', 'duration': 120.0, 'name': 'Just some local audio that is 2mins long'}
{'url': 'F:\\Music\\whatever.m4a', 'duration': None, 'name': 'absolute path on Windows'}
{'url': '%UserProfile%\\Music\\short.ogg', 'duration': 5.0, 'name': 'example for an Environment variable'}
```
Вывод (.opml):
```
{'type': 'rss', 'text': 'CNET News.com', 'xml_url': 'http://news.com.com/2547-1_3-0-5.xml', 'description': 'Tech news and business reports by CNET News.com. Focused on information technology, core topics include computers, hardware, software, networking, and Internet media.', 'html_url': 'http://news.com.com/', 'language': 'unknown', 'title': 'CNET News.com', 'version': 'RSS2'}
{'type': 'rss', 'text': 'washingtonpost.com - Politics', 'xml_url': 'http://www.washingtonpost.com/wp-srv/politics/rssheadlines.xml', 'description': 'Politics', 'html_url': 'http://www.washingtonpost.com/wp-dyn/politics?nav=rss_politics', 'language': 'unknown', 'title': 'washingtonpost.com - Politics', 'version': 'RSS2'}
{'type': 'rss', 'text': 'Scobleizer: Microsoft Geek Blogger', 'xml_url': 'http://radio.weblogs.com/0001011/rss.xml', 'description': "Robert Scoble's look at geek and Microsoft life.", 'html_url': 'http://radio.weblogs.com/0001011/', 'language': 'unknown', 'title': 'Scobleizer: Microsoft Geek Blogger', 'version': 'RSS2'}
{'type': 'rss', 'text': 'Yahoo! News: Technology', 'xml_url': 'http://rss.news.yahoo.com/rss/tech', 'description': 'Technology', 'html_url': 'http://news.yahoo.com/news?tmpl=index&amp;cid=738', 'language': 'unknown', 'title': 'Yahoo! News: Technology', 'version': 'RSS2'}
{'type': 'rss', 'text': 'Workbench', 'xml_url': 'http://www.cadenhead.org/workbench/rss.xml', 'description': 'Programming and publishing news and comment', 'html_url': 'http://www.cadenhead.org/workbench/', 'language': 'unknown', 'title': 'Workbench', 'version': 'RSS2'}
{'type': 'rss', 'text': 'Christian Science Monitor | Top Stories', 'xml_url': 'http://www.csmonitor.com/rss/top.rss', 'description': 'Read the front page stories of csmonitor.com.', 'html_url': 'http://csmonitor.com', 'language': 'unknown', 'title': 'Christian Science Monitor | Top Stories', 'version': 'RSS'}
{'type': 'rss', 'text': 'Dictionary.com Word of the Day', 'xml_url': 'http://www.dictionary.com/wordoftheday/wotd.rss', 'description': 'A new word is presented every day with its definition and example sentences from actual published works.', 'html_url': 'http://dictionary.reference.com/wordoftheday/', 'language': 'unknown', 'title': 'Dictionary.com Word of the Day', 'version': 'RSS'}
{'type': 'rss', 'text': 'The Motley Fool', 'xml_url': 'http://www.fool.com/xml/foolnews_rss091.xml', 'description': 'To Educate, Amuse, and Enrich', 'html_url': 'http://www.fool.com', 'language': 'unknown', 'title': 'The Motley Fool', 'version': 'RSS'}
{'type': 'rss', 'text': 'InfoWorld: Top News', 'xml_url': 'http://www.infoworld.com/rss/news.xml', 'description': 'The latest on Top News from InfoWorld', 'html_url': 'http://www.infoworld.com/news/index.html', 'language': 'unknown', 'title': 'InfoWorld: Top News', 'version': 'RSS2'}
{'type': 'rss', 'text': 'NYT > Business', 'xml_url': 'http://www.nytimes.com/services/xml/rss/nyt/Business.xml', 'description': 'Find breaking news & business news on Wall Street, media & advertising, international business, banking, interest rates, the stock market, currencies & funds.', 'html_url': 'http://www.nytimes.com/pages/business/index.html?partner=rssnyt', 'language': 'unknown', 'title': 'NYT > Business', 'version': 'RSS2'}
{'type': 'rss', 'text': 'NYT > Technology', 'xml_url': 'http://www.nytimes.com/services/xml/rss/nyt/Technology.xml', 'description': '', 'html_url': 'http://www.nytimes.com/pages/technology/index.html?partner=rssnyt', 'language': 'unknown', 'title': 'NYT > Technology', 'version': 'RSS2'}
{'type': 'rss', 'text': 'Scripting News', 'xml_url': 'http://www.scripting.com/rss.xml', 'description': "It's even worse than it appears.", 'html_url': 'http://www.scripting.com/', 'language': 'unknown', 'title': 'Scripting News', 'version': 'RSS2'}
{'type': 'rss', 'text': 'Wired News', 'xml_url': 'http://www.wired.com/news_drop/netcenter/netcenter.rdf', 'description': 'Technology, and the way we do business, is changing the world we know. Wired News is a technology - and business-oriented news service feeding an intelligent, discerning audience. What role does technology play in the day-to-day living of your life? Wired News tells you. How has evolving technology changed the face of the international business world? Wired News puts you in the picture.', 'html_url': 'http://www.wired.com/', 'language': 'unknown', 'title': 'Wired News', 'version': 'RSS'}
```
Длительность (duration) указывается в секундах, непонятно насколько точно. Длительность равная -1.0
означает, что ссылка (url) указывает на потоковое аудио.