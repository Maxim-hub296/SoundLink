import os

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4


def is_file_size_allowed(file_path) -> bool:
    return 20 <= os.path.getsize(file_path) <= 20 * 1024 * 1024


def extract_audio_metadata(file_path) -> dict[str, None]:
    ext = os.path.splitext(file_path)[1].lower()
    metadata = {
        'title': None,
        'artist': None,
        'length': None,
    }

    try:
        if ext == '.mp3':
            audio = EasyID3(file_path)
            metadata['title'] = audio.get('title', [None])[0]
            metadata['artist'] = audio.get('artist', [None])[0]
            mp3 = MP3(file_path)
            metadata['length'] = int(mp3.info.length)

        elif ext in ('.m4a', '.aac', '.mp4'):
            audio = MP4(file_path)
            metadata['title'] = audio.get('title', [None])[0]
            metadata['artist'] = audio.get('artist', [None])[0]
            metadata['length'] = int(audio.info.length)

        elif ext == '.flac':
            audio = FLAC(file_path)
            metadata['title'] = audio.get('title', [None])[0]
            metadata['artist'] = audio.get('artist', [None])[0]
            metadata['length'] = int(audio.info.length)

    except Exception:
        pass

    return metadata


def delete_audio_file(file_path) -> bool:
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        return False


def is_allowed_file_type(file_path) -> bool:
    ext = os.path.splitext(file_path)[1].lower()
    allowed_types = ["mp3", "flac", "wav"]
    if ext not in allowed_types:
        return False
    return True
