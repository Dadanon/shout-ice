import os
import re
from typing import List, Optional

from exceptions import PlaylistExtensionError, DirectiveError, OPMLVersionError

RIGHT_EXTENSIONS = ['.m3u', '.m3u8', '.pls', '.opml']
"""Валидные разрешения файлов, содержащих плейлисты"""

patterns = {
    'get_outline_type': r'type="(.*?)"',
    'get_outline_text': r'text="(.*?)"',
    'get_outline_xml_url': r'xmlUrl="(.*?)"',
    'get_outline_description': r'description="(.*?)"',
    'get_outline_html_url': r'htmlUrl="(.*?)"',
    'get_outline_language': r'language="(.*?)"',
    'get_outline_title': r'title="(.*?)"',
    'get_outline_version': r'version="(.*?)"'
}


class PlaylistRecord:
    """Класс, представляющий собой запись в плейлисте
    с обязательным url и опциональными параметрами"""
    url: str
    duration: Optional[float]
    name: Optional[str]

    def __init__(self, url: str, duration: Optional[float] = None, name: Optional[str] = None):
        self.url = url
        self.duration = duration
        self.name = name


class OPMLRecord:
    """Класс, представляющий собой запись из тега outline
    с обязательными и опциональными параметрами"""
    type: str
    text: str
    xml_url: str
    description: Optional[str]
    html_url: Optional[str]
    language: Optional[str]
    title: Optional[str]
    version: Optional[str]

    def __init__(self,
                 o_type: str,
                 o_text: str,
                 o_xml_url: str,
                 o_description: Optional[str] = None,
                 o_html_url: Optional[str] = None,
                 o_language: Optional[str] = None,
                 o_title: Optional[str] = None,
                 o_version: Optional[str] = None
                 ):
        self.type = o_type
        self.text = o_text
        self.xml_url = o_xml_url
        self.description = o_description
        self.html_url = o_html_url
        self.language = o_language
        self.title = o_title
        self.version = o_version


def get_opml_list(opml_path: str) -> List[OPMLRecord]:
    playlist: List[OPMLRecord] = []
    with open(opml_path, "r") as f:
        content = f.read()
    opml_version_match = re.search(r'<opml version="2.0"|\'2.0\'>', content, re.DOTALL)
    if not opml_version_match:
        raise OPMLVersionError("Версия opml файла отлична от 2.0")
    outline_matches = re.finditer(r'<outline (.*?)>|/>', content, re.DOTALL)
    for outline_match in outline_matches:
        outline = outline_match.group(0)
        type_match = re.search(patterns['get_outline_type'], outline)

        if not type_match:
            continue
        if (o_type := type_match.group(1)) != "rss":
            continue

        o_text_match = re.search(patterns['get_outline_text'], outline)
        o_xml_url_match = re.search(patterns['get_outline_xml_url'], outline)
        o_description_match = re.search(patterns['get_outline_description'], outline)
        o_html_url_match = re.search(patterns['get_outline_html_url'], outline)
        o_language_match = re.search(patterns['get_outline_language'], outline)
        o_title_match = re.search(patterns['get_outline_title'], outline)
        o_version_match = re.search(patterns['get_outline_version'], outline)

        o_text = _get_sanitized_text(o_text_match.group(1))
        o_xml_url = o_xml_url_match.group(1)
        o_description = _get_sanitized_text(o_description_match.group(1)) if o_description_match else None
        o_html_url = o_html_url_match.group(1) if o_html_url_match else None
        o_language = o_language_match.group(1) if o_language_match else None
        o_title = _get_sanitized_text(o_title_match.group(1)) if o_title_match else None
        o_version = o_version_match.group(1) if o_version_match else None

        opml_record: OPMLRecord = OPMLRecord(o_type, o_text, o_xml_url, o_description, o_html_url, o_language, o_title, o_version)
        playlist.append(opml_record)
    return playlist


def get_extension(path: str) -> str:
    file_extension = os.path.splitext(path)[1]
    if file_extension not in RIGHT_EXTENSIONS:
        raise PlaylistExtensionError(
            f"Формат файла не предназначен для хранения плейлистов, расширение: {file_extension}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Отсутствует файл по пути: {path}")
    return file_extension


def get_m3u_list(m3u_path: str) -> List[PlaylistRecord]:
    playlist: List[PlaylistRecord] = []
    with open(m3u_path, "r") as f:
        content = f.read()
    if not content.startswith('#EXTM3U'):
        print('A simple, not extended m3u is opening...')

    content = re.sub(r'#EXTM3U\n{1,}', '', content)  # Удаляем основную директиву, чтобы не мешала
    # Находим для начала записи с #EXTINF, добавляем их в список, а затем удаляем
    extinf_record_matches = re.finditer(r'#EXTINF:(.*?)\n{1,}(.*?)\n', content, re.DOTALL)
    for record_match in extinf_record_matches:
        record_data, record_url = record_match.group(1), record_match.group(2)
        record_duration, record_name = record_data.split(',')
        extinf_record = PlaylistRecord(record_url, float(record_duration), record_name)
        playlist.append(extinf_record)
        content = content.replace(record_match.group(0), '')

    # Теперь находим оставшиеся записи без extinf
    content = re.sub(r'\n{2,}', '\n', content)  # Удаляем оставшиеся пустые строки
    remaining_records = content.split('\n')
    for remaining_record in remaining_records:
        no_extinf_record = PlaylistRecord(remaining_record)
        playlist.append(no_extinf_record)

    return playlist


def get_pls_list(pls_path: str) -> List[PlaylistRecord]:
    playlist: List[PlaylistRecord] = []
    with open(pls_path, "r") as f:
        content = f.read()
    if not content.startswith('[playlist]'):
        raise DirectiveError("Отсутствует директива [playlist] в начале pls файла")
    pattern = re.compile(
        r'File(?P<num>\d+)=(?P<file>.+)\n?'
        r'(Title(?P=num)=(?P<title>.+))?\n?'
        r'(Length(?P=num)=(?P<length>.+))?\n?',
        re.MULTILINE
    )

    matches = pattern.finditer(content)

    for match in matches:
        url = match.group('file')
        title = match.group('title')
        length = match.group('length')

        # Заменяем отсутствующие значения на None
        title = title if title else None
        length = float(length) if length else None
        playlist.append(PlaylistRecord(url, length, title))
    return playlist


def _get_sanitized_text(text: str) -> str:
    pretty_text = (
        text
        .replace('&lt;', '<')
        .replace('&gt;', '>')
        .replace('\r\n', ' ')
        .replace('\n', ' ')
        .replace('&nbsp;', ' ')
        .replace(u'\xa0', u' ')
        .replace('&mdash;', '-')
        .replace('&laquo;', '"')
        .replace('&raquo;', '"')
        .replace('&apos;', '\'')
        .replace('&quot;', '"')
        .replace('&#8230;', '…')
        .replace('&amp;', '&')
        .replace('&#39;', '\'')
    )

    pretty_text = re.sub('\s+', ' ', pretty_text)

    return pretty_text
