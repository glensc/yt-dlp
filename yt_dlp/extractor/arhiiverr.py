from .common import InfoExtractor
from .. import int_or_none
from ..utils import (
    traverse_obj,
    unified_timestamp,
)


class ArhiivErrIE(InfoExtractor):
    _VALID_URL = r'https://arhiiv\.err\.ee/video/vaata/(?P<id>.+)$'
    _TESTS = [{
        'note': 'S01E06: Impulss',
        'url': 'https://arhiiv.err.ee/video/vaata/pealtnagija-481',
        'md5': '1ff59d535310ac9c5cf5f287d8f91b2d',
        'info_dict': {
            'id': '1609145945',
            'ext': 'mp4',
            'title': 'Loteriipilet hooldekodusse',
            'description': 'md5:d1770e868afffd5d42b886283574941e',
            'upload_date': '20231107',
            'timestamp': 1699380000,
            'series': 'Impulss',
            'season': 'Season 1',
            'season_number': 1,
            'episode': 'Loteriipilet hooldekodusse',
            'episode_number': 6,
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        content_url = f"https://arhiiv.err.ee/api/v1/content/video/{video_id}"
        data = self._download_json(content_url, video_id)

        return {
            'id': video_id,
            'title': traverse_obj(data, ('info', 'title')),
            'description': traverse_obj(data, ('info', 'description')),
            'formats': self._extract_m3u8_formats(traverse_obj(data, ('media', 'src', 'hls')), video_id),
            'timestamp': unified_timestamp(traverse_obj(data, ('info', 'date'))),
            'series': traverse_obj(data, ('info', 'seriesTitle')),
            'episode': traverse_obj(data, ('info', 'title')),
            'episode_number': int_or_none(traverse_obj(data, ('info', 'episode'))),
        }
