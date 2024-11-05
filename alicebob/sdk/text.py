import re

from typing import List

import html2text_rs

REGEX_LINKS = re.compile(r'href=[\"\']([^\"\']+)[\"\']')


def extract_urls_from_html(content: str, filters: tuple) -> List[str]:
    """
    Extract all the URL from an HTML content excluding the ones that contains any of the filters.

    :param content: HTML content
    :param filters: Tuple of strings to exclude
    """
    found = REGEX_LINKS.findall(content, re.M | re.I) or []

    if found:
        for x in found:
            if filters and any(f in x for f in filters):
                continue

            else:
                yield x


def parse_html(content: str) -> str:
    """
    Get an HTML content, recover the <body> tag, convert it to text and return it
    """
    regex = r'<body[^>]*>(.*?)</body>'

    matches = re.search(regex, content, re.MULTILINE | re.DOTALL)

    if not matches:
        raise ValueError("No body tag found")

    if not matches.group(1):
        raise ValueError("Empty body tag")

    return html2text_rs.text_plain(matches.group(1))


__all__ = ("extract_urls_from_html", "parse_html")
