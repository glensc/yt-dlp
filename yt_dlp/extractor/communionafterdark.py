import re

from .jupiter import JupiterIE
from ..utils import (
    try_call, extract_attributes, get_element_text_and_html_by_tag,
    get_elements_by_class,
    clean_html, unified_timestamp, unified_strdate,
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

    @staticmethod
    def extract_url(webpage):
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

    @staticmethod
    def extract_description_and_title(webpage):
        divs = try_call(lambda: get_elements_by_class("sqs-html-content", webpage))
        tag = try_call(lambda: [tag for tag in divs or [] if "Tracklisting" in tag][0])

        p = [clean_html(c.strip()) for c in re.findall(r'(?s)<p.*?>(.*?)</p>', tag)]
        title = p.pop(0).replace("Tracklisting ", "")

        return title, "\n".join(p)

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        title, description = self.extract_description_and_title(webpage)
        audio_url = self.extract_url(webpage)
        timestamp = self._html_search_meta('datePublished', webpage, default=None)
        upload_date = unified_strdate(timestamp)
        author = self._html_search_meta('author', webpage, default=None)

        res = {
            'id': video_id,
            'title': title,
            'description': description,
            'url': audio_url,
            'timestamp': unified_timestamp(timestamp),
            'upload_date': upload_date,
            'release_date': upload_date,
            'uploader': author,
            'was_live': True,
        }
        import json
        print(json.dumps(res))
        return res
