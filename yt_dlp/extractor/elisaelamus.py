import json

from .common import InfoExtractor
from .. import int_or_none
from ..utils import (
    traverse_obj,
)


class ElisaElamusIE(InfoExtractor):
    _VALID_URL = r'https://elisaelamus\.ee(?:/huub)?/seriaalid/(?P<id>crid:[^?]+)'
    _TESTS = [{
        'url': 'https://elisaelamus.ee/seriaalid/crid:~~2F~~2Fschange~dotcom~~2F9469d800-ee7b-4e2a-8980-6303a3f68831?episode=crid%3A%7E%7E2F%7E%7E2Fschange.com%7E%7E2Fteeveekolm.ee%7E%7E2FTEEB2024020716150058',
        'md5': '1ff59d535310ac9c5cf5f287d8f91b2d',
        'info_dict': {
            'id': '1609145945',
            'ext': 'mp4',
            'title': 'Loteriipilet hooldekodusse',
            'description': 'md5:fa8a2ed0cdccb130211513443ee4d571',
            'upload_date': '20231107',
            'timestamp': 1699380000,
            'series': 'Impulss',
            'season': 'Season 1',
            'season_number': 1,
            'episode': 'Loteriipilet hooldekodusse',
            'episode_number': 6,
            'series_id': 1609108187,
            'release_year': 2023,
            'episode_id': 1609145945,
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        data = self.get_data(video_id)

        import json
        res = {
            **traverse_obj(data, {
                'title': 'heading',
                'description': 'lead',
                'release_year': ('year', {int_or_none}),
                'timestamp': 'publicStart',
            })
        }
        print(json.dumps(res))
        return res
