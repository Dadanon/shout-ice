import os
import re
from typing import List, Optional, Callable

from exceptions import PlaylistExtensionError, DirectiveError


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


def get_extension_callable(path: str) -> Callable:
    file_extension = os.path.splitext(path)[1]
    right_extensions = ['.m3u', '.m3u8'] if file_extension == '.m3u' else ['.pls'] if file_extension == '.pls' else []
    if file_extension not in right_extensions:
        raise PlaylistExtensionError(
            f"Формат файла не предназначен для хранения плейлистов, расширение: {file_extension}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Отсутствует файл по пути: {path}")
    return CORR_FUNCTIONS.get(file_extension)


def get_m3u_list(m3u_path: str) -> List[PlaylistRecord]:
    playlist: List[PlaylistRecord] = []
    get_extension_callable(m3u_path)
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
    get_extension_callable(pls_path)
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


CORR_FUNCTIONS = {
    '.m3u': get_m3u_list,
    '.m3u8': get_m3u_list,
    '.pls': get_pls_list
}
