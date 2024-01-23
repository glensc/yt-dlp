from .jupiter import JupiterIE
from .. import int_or_none
from ..utils import (
    traverse_obj, try_call, extract_attributes, get_element_text_and_html_by_tag, ExtractorError,
    get_elements_text_and_html_by_attribute, get_elements_by_class,
)


class CommunionAfterDarkIE(JupiterIE):
    _VALID_URL = r'https://www\.communionafterdark\.com/listennow/(?P<id>[\d\w]+)'
    _TESTS = [{
        'url': 'https://www.communionafterdark.com/listennow/535kxa6akttbzhkxblzbawr46esabw',
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

    def extract_url(self, url, video_id):
        webpage = self._download_webpage(url, video_id)
        tags = try_call(lambda: get_elements_by_class('sqs-html-content', webpage))
        if not tags:
            return None

        for tag in tags:
            link = try_call(lambda: extract_attributes(get_element_text_and_html_by_tag('a', tag)[1])['href'])
            if not link:
                continue
            if "https://www.buzzsprout.com/" not in link:
                continue
            return link

    def _real_extract(self, url):
        video_id = self._match_id(url)
        audio_url = self.extract_url(url, video_id)

        raise RuntimeError()
