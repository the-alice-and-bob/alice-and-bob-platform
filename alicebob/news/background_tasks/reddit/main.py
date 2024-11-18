from typing import Iterable

import requests

from alicebob_sdk import News, SummarizedNews, extract_urls_from_html, parse_html, summarize_with_ia, find_news


# Provider :: REDDIT
def main(news: News) -> Iterable[SummarizedNews]:
    # Extract all the URL from an HTML content

    # download the content for each news

    print(f"[*] Processing Reddit news: {news.title}")
    for url in extract_urls_from_html(news.summary, ("reddit.com", "reddit.it")):

        if find_news(news):
            print(f"[!] News already processed: {news.title}")
            continue

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error downloading content from {url}")
            continue

        site_content = response.text
        plain_text = parse_html(site_content)

        tags, linkedin, twitter, _ = summarize_with_ia(site_content, plain_text)

        # Parse the "origin"
        origin = news.origin.replace("https://www.reddit.com", "")
        if origin.endswith("/"):
            origin = origin[:-1]

        yield SummarizedNews(
            title=news.title,
            linkedin=linkedin,
            twitter=twitter,
            tags=tags,
            url=url,
            published=news.published,
            provider=news.provider.name.lower(),
            origin=news.origin
        )
