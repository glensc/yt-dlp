from .common import InfoExtractor
from ..utils import (
    traverse_obj,
    int_or_none,
    url_or_none,
    parse_iso8601,
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

        return {
            'id': video_id,
            'formats': formats,
            'subtitles': subtitles,
            **traverse_obj(data, {
                'title': ('showInfo', 'programSubTitle', {str}),
                'description': ('showInfo', 'programLead', {str}),
                'thumbnail': ('showInfo', 'media', 'thumbnail', 'url', {url_or_none}),
                'timestamp': ('seoData', 'ogPublishTime', {parse_iso8601}),
                'series': ('showInfo', 'programName', {str}),
                'season_number': ('pageControlData', 'mainContent', 'season', {int_or_none}),
                'episode': ('showInfo', 'programSubTitle', {str}),
                'episode_number': ('pageControlData', 'mainContent', 'episode', {int_or_none}),
            }),
        }
