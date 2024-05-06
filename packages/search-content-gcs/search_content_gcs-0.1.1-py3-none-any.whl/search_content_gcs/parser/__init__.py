from typing import List

from ..models import SimpleYouTubeData
from ..models.google_custom_search import Response, Item
from ..utils.youtube_url import parse_video_id_from_url


# JSON 데이터를 모델로 파싱


def parse_search_result(data: dict):
    result = Response.parse_obj(data)
    return result


def parse_youtube_data_from_cse(items: List[Item]) -> List[SimpleYouTubeData]:
    extracted_data = []
    for item in items:
        ids = parse_video_id_from_url(item.link)
        video_id = ids.get('video_id')
        channel_id = ids.get('channel_id')
        shorts_id = ids.get('shorts_id')
        type_ = ids.get('type')  # 데이터 유형 추출

        simple_data = SimpleYouTubeData(
            title=item.title,
            snippet=item.snippet,
            url=item.link,
            video_id=video_id,
            channel_id=channel_id,
            shorts_id=shorts_id,
            type=type_
        )
        extracted_data.append(simple_data)
    return extracted_data


__all__ = [parse_search_result, parse_youtube_data_from_cse]