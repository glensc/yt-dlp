import json

from .common import InfoExtractor
from .. import int_or_none
from ..utils import (
    traverse_obj, join_nonempty,
)


class ElisaElamusIE(InfoExtractor):
    _VALID_URL = r'https://elisaelamus\.ee(?:/huub)?/seriaalid/(?P<id>crid[^?]+)\?episode=(?P<ep>crid[^$]+)'
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

    def episode_index(self, data, episode_id: str):
        """
        Return index of Series.ChildSeriesCollection,Series.Titles.Title.id that matches episode_id
        """
        id_only = episode_id.split(r'~~')[-1]
        serie = traverse_obj(data, ('Series', 'ChildSeriesCollection', 'Series'))[0]
        titles = traverse_obj(serie, ('Titles', 'Title'))
        return [i for i, t in enumerate(titles, start=1) if t["id"].endswith(id_only)][0]

    def _real_extract(self, url):
        telecast_id, episode = self._match_valid_url(url).group('id', 'ep')
        episode = episode.replace("%3A", ":").replace("%7E", "~")
        video_id = join_nonempty(telecast_id, episode, delim='_')
        data = self.get_data(video_id)

        import json
        res = {
            'id': video_id,
            'age_limit':  18 if traverse_obj(data, ('Series', 'IsAdult')) else None,
            **traverse_obj(data, {
                'title': ('Series', 'Name'),
                'series':  ('Series', 'Name'),
                'season':  ('Series', 'ChildSeriesCollection', 'Series', 'Name'),
            }),
            'episode_number': self.episode_index(data, episode),
        }
        print(json.dumps(res))
        return res
