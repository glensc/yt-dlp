import re

from .common import InfoExtractor
from ..utils import (
    try_call, extract_attributes, get_element_text_and_html_by_tag,
    get_elements_by_class,
    clean_html, unified_timestamp, unified_strdate,
)


class CommunionAfterDarkListingIE(InfoExtractor):
    _VALID_URL = r'https://www\.communionafterdark\.com/listennow(\?offset=(?P<offset>\d+))?'
    _TESTS = [{
        'url': 'https://www.communionafterdark.com/listennow',
        'md5': '583a75874aa1fa1368eecad4dc225532',
        'info_dict': {
            'id': '535kxa6akttbzhkxblzbawr46esabw',
            'ext': 'mp3',
            'title': 'January 22nd, 2024',
            'description': 'md5:7c420a1c1ec6a51b861594e7b71041be',
            'upload_date': '20240122',
            'release_date': '20240122',
            'timestamp': 1705939304,
            'uploader': 'Sherri Maus',
            'release_year': 2024,
        },
    }, {
        'url': 'https://www.communionafterdark.com/listennow?offset=1694443682010',
        'md5': '583a75874aa1fa1368eecad4dc225532',
        'info_dict': {
            'id': '535kxa6akttbzhkxblzbawr46esabw',
            'ext': 'mp3',
            'title': 'January 22nd, 2024',
            'description': 'md5:7c420a1c1ec6a51b861594e7b71041be',
            'upload_date': '20240122',
            'release_date': '20240122',
            'timestamp': 1705939304,
            'uploader': 'Sherri Maus',
            'release_year': 2024,
        },
    }]

    def _real_extract(self, url):
        offset = self._match_valid_url(url).group('offset')
        page_id = f"index at {offset}" if offset else "latest index"
        webpage = self._download_webpage(url, page_id)

        tags = try_call(lambda: get_elements_by_class('BlogList-item-image', webpage))
        if not tags:
            return None

        links = []
        for tag in tags:
            link: str | None = try_call(
                lambda: extract_attributes(get_element_text_and_html_by_tag('a', tag)[1])['href'])
            if not link:
                continue
            if link.startswith('/listennow/'):
                links.append(f'https://www.communionafterdark.com{link}')

        return self.playlist_result(
            playlist_title=page_id,
            entries=[self.url_result(link) for link in links]
        )


class CommunionAfterDarkIE(InfoExtractor):
    _VALID_URL = r'https://www\.communionafterdark\.com/listennow/(?P<id>[\d\w]+)'
    _TESTS = [{
        'url': 'https://www.communionafterdark.com/listennow/535kxa6akttbzhkxblzbawr46esabw',
        'md5': '583a75874aa1fa1368eecad4dc225532',
        'info_dict': {
            'id': '535kxa6akttbzhkxblzbawr46esabw',
            'ext': 'mp3',
            'title': 'January 22nd, 2024',
            'description': 'md5:7c420a1c1ec6a51b861594e7b71041be',
            'upload_date': '20240122',
            'release_date': '20240122',
            'timestamp': 1705939304,
            'uploader': 'Sherri Maus',
            'release_year': 2024,
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
        tag = try_call(lambda: [tag for tag in divs or [] if "Tracklisting" in tag or "Track listing" in tag][0])
        if tag is None:
            raise RuntimeError("Failed to find track listing")

        p = [clean_html(c.strip()) for c in re.findall(r'(?s)<p.*?>(.*?)</p>', tag)]
        title = p.pop(0)
        title = re.sub(r'Track\s?listing\s*?', '', title).strip()

        return title, "\n".join(p)

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        title, description = self.extract_description_and_title(webpage)
        audio_url = self.extract_url(webpage)
        timestamp = self._html_search_meta('datePublished', webpage, default=None)
        upload_date = unified_strdate(timestamp)
        author = self._html_search_meta('author', webpage, default=None)

        return {
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
