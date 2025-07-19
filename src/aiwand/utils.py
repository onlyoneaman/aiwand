import json
from typing import Any
from urllib.parse import urlparse

def convert_to_string(content: Any) -> str:
    """Convert any content to string representation."""
    if isinstance(content, str):
        return content
    elif isinstance(content, (dict, list)):
        try:
            return json.dumps(content, indent=2, ensure_ascii=False)
        except (TypeError, ValueError):
            return str(content)
    else:
        return str(content)
    
def string_to_json(content: str) -> dict:
    """Clean the JSON response from the AI."""
    try:
        cleaned = content.strip("`").split("\n", 1)[1].rsplit("\n", 1)[0]
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return content

def is_url(link: str) -> bool:
    """Check if a link is a URL (starts with http/https)."""
    return link.strip().startswith(('http://', 'https://', 'www.')) 


def is_local_file(path: str) -> bool:
    parsed = urlparse(path)
    return parsed.scheme == '' or parsed.scheme == 'file'
