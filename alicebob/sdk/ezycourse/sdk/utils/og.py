import re

from urllib.parse import urlparse
from dataclasses import dataclass

import requests

# use simple regex, no need for lxml
META_TAG = re.compile(r'<meta[^>]+content=[^>]+>', re.U | re.I)
META_ATTR = re.compile(
    r'(name|property|content)=(?:\'|\")(.*?)(?:\'|\")',
    re.U | re.I | re.S
)
TITLE = re.compile(r'<title>(.*?)</title>', re.U | re.I | re.S)


@dataclass
class OpenGraph:
    locale: str = None
    type: str = None
    title: str = None
    url: str = None
    site_name: str = None
    image: str = None
    image_width: int = None
    image_height: int = None
    image_type: str = None


class OpenGraphException(Exception):
    pass


def extract_og(url: str) -> OpenGraph:
    """
    Extract OpenGraph data from a given URL
    """
    try:
        content = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    except requests.exceptions.RequestException:
        raise OpenGraphException("Failed to fetch the page")

    head = content.split('</head>', 1)[0]

    def parse_opengraph(key: str, _content: str, og_object: OpenGraph):
        og_properties = (
            "og:locale",
            "og:type",
            "og:title",
            "og:url",
            "og:site_name",
            "og:image",
            "og:image:width",
            "og:image:height",
            "og:image:type"
        )

        if key not in og_properties:
            return False

        clean_name = key.replace("og:", "").replace(":", "_")

        if clean_name == "url":
            if not _content.startswith("/"):
                _content = "/" + _content

            # get base url from the original url
            parsed_url = urlparse(url)
            _content = f"{parsed_url.scheme}://{parsed_url.netloc}{_content}"

        setattr(og_object, clean_name, _content)

    def parse_twitter(key: str, _content: str, og_object: OpenGraph):
        twitter_properties = (
            "twitter:card",
            "twitter:site",
            "twitter:creator",
            "twitter:title",
            "twitter:description",
            "twitter:image",
            "twitter:image:alt"
        )

        if key not in twitter_properties:
            return False

        clean_name = key.replace("twitter:", "").replace(":", "_")

        setattr(og_object, clean_name, _content)

    def parse_linkedin(key: str, _content: str, og_object: OpenGraph):
        linkedin_properties = (
            "linkedin:title",
            "linkedin:description",
            "linkedin:image",
            "linkedin:image:width",
            "linkedin:image:height",
            "linkedin:image:type"
        )

        if key not in linkedin_properties:
            return False

        clean_name = key.replace("linkedin:", "").replace(":", "_")

        setattr(og_object, clean_name, _content)

    og = OpenGraph()

    for text in META_TAG.findall(head):
        try:
            kv = dict(META_ATTR.findall(text))
        except ValueError:
            continue

        try:
            prop = kv['property']
        except KeyError:
            continue

        try:
            c = kv['content']
        except KeyError:
            continue

        parse_opengraph(prop, c, og)
        parse_twitter(prop, c, og)
        parse_linkedin(prop, c, og)

    if not og.title:
        m = TITLE.findall(head)
        if m:
            og.title = m[0]

    if not og.image:
        # Try to get the image from page icon. Split "href" in a group. Multiline
        # m = re.search(r'(<link\s+rel=[\"\']\w+icon.*)(href=[\"\'])(.*)([\"\']+/>)', head, re.U | re.I | re.M)
        m = re.search(r'<link[^>]*\brel=["\'][^"\']*icon[^"\']*["\'][^>]*\bhref=["\']([^"\']+)["\']', head)
        if m:
            try:
                icon = m.group(1)
                og.image = icon
            except ValueError:
                pass

    return og


__all__ = ('extract_og',)
