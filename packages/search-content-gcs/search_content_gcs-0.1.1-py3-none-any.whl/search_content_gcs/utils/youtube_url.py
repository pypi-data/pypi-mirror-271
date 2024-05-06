from urllib.parse import parse_qs, urlparse

from pydantic import HttpUrl


def parse_video_id_from_url(url: HttpUrl) -> dict:
    query_params = parse_qs(url.query)
    path_parts = url.path.split('/')
    result = {}

    if "watch" in path_parts:
        result['video_id'] = query_params.get('v', [None])[0]
        result['type'] = 'video'
    elif "shorts" in path_parts:
        result['shorts_id'] = path_parts[path_parts.index("shorts") + 1]
        result['type'] = 'shorts'
    elif "channel" in path_parts:
        result['channel_id'] = path_parts[path_parts.index("channel") + 1]
        result['type'] = 'channel'
    return result
