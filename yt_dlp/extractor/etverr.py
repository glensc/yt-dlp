from .common import InfoExtractor
from .. import int_or_none
from ..utils import (
    traverse_obj,
    unified_timestamp,
)


class ArhiivErrIE(InfoExtractor):
    # _VALID_URL = r'https://arhiiv\.err\.ee/video/vaata/(?P<id>.+)$'
    _VALID_URL = r'https://etv\.err\.ee/(?P<id>\d+)/'
    _TESTS = [{
        'url': 'https://etv.err.ee/1609138376/pealtnagija',
        'md5': '1ff59d535310ac9c5cf5f287d8f91b2d',
        'info_dict': {
            'id': 'pealtnagija-481',
            'ext': 'mp4',
            'title': 'Pealtnägija : 481',
            'description': 'md5:d41d8cd98f00b204e9800998ecf8427e',
            'upload_date': '20121114',
            'timestamp': 1352851200,
            'series': 'Pealtnägija',
            'episode': 'Pealtnägija : 481',
            'episode_number': 481,
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        # content_url = f"https://etv.err.ee/api/tv/getTvPageData?contentId={video_id}&parentContentId=1038446&categoryDataOnly=false"
        content_url = f"https://etv.err.ee/api/tv/getTvPageData?contentId={video_id}"
        data = self._download_json(content_url, video_id)

        return {
            'id': video_id,
            'title': traverse_obj(data, ('showInfo', 'programSubTitle')),
            'description': traverse_obj(data, ('showInfo', 'programLead')),
            'thumbnail': traverse_obj(data, ('showInfo', 'media', 'thumbnail', 'url')),
            'formats': self._extract_m3u8_formats(traverse_obj(data, ('showInfo', 'media', 'src', 'hls')), video_id),
            'timestamp': traverse_obj(data, ('seoData', 'ogPublishTime')),
            'series': traverse_obj(data, ('showInfo', 'programName')),
            'season_number': int_or_none(traverse_obj(data, ('pageControlData', 'mainContent', 'season'))),
            'episode': traverse_obj(data, ('showInfo', 'programSubTitle')),
            'episode_number': int_or_none(traverse_obj(data, ('pageControlData', 'mainContent', 'episode'))),
        }
