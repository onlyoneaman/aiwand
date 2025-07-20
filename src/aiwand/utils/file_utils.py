from urllib.parse import urlparse


def is_local_file(path: str) -> bool:
    path = path.strip()
    parsed = urlparse(path)
    return parsed.scheme == 'file'
