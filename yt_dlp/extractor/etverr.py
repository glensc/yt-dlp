from .common import InfoExtractor
from ..utils import (
    traverse_obj,
    int_or_none,
    unified_timestamp,
)


class EtvErrIE(InfoExtractor):
    _VALID_URL = r'https://etv\.err\.ee/(?P<id>\d+)/'
    _TESTS = [{
        'url': 'https://etv.err.ee/1609138376/pealtnagija',
        'md5': '1ff59d535310ac9c5cf5f287d8f91b2d',
        'info_dict': {
            'id': '1609138376',
            'ext': 'mp4',
            'title': '25. hooaeg, 877. osa | ',
            'description': 'md5:03ff09755be13df4d5f9848f38e30dc9',
            'upload_date': '20231101',
            'timestamp': 1698861900,
            'series': 'Pealtnägija',
            'episode': '25. hooaeg, 877. osa | ',
            'episode_number': 877,
            'season': 'Season 25',
            'season_number': 25,
            'thumbnail': r're:^https://.+\.jpg',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        content_url = f"https://etv.err.ee/api/tv/getTvPageData?contentId={video_id}"
        data = self._download_json(content_url, video_id)
        hls = traverse_obj(data, ('showInfo', 'media', 'src', 'hls'))
        formats, subtitles = self._extract_m3u8_formats_and_subtitles(hls, video_id)
        timestamp = unified_timestamp(traverse_obj(data, ('seoData', 'ogPublishTime')))
        print(timestamp)

        return {
            'id': video_id,
            'title': traverse_obj(data, ('showInfo', 'programSubTitle')),
            'description': traverse_obj(data, ('showInfo', 'programLead')),
            'thumbnail': traverse_obj(data, ('showInfo', 'media', 'thumbnail', 'url')),
            'formats': formats,
            'subtitles': subtitles,
            'timestamp': timestamp,
            'series': traverse_obj(data, ('showInfo', 'programName')),
            'season_number': int_or_none(traverse_obj(data, ('pageControlData', 'mainContent', 'season'))),
            'episode': traverse_obj(data, ('showInfo', 'programSubTitle')),
            'episode_number': int_or_none(traverse_obj(data, ('pageControlData', 'mainContent', 'episode'))),
        }
