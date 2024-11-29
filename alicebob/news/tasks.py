# from typing import Iterable
#
# import decouple
#
# from celery import shared_task
#
# from alicebob_sdk import NewsProvider, InoReader, News, publish_to_notion, notify_pushover
#
# # Providers:
# from .background_tasks.reddit.main import main as provider_reddit_news
# from .background_tasks.apisecurity.main import main as provider_api_security_news
#
# PROVIDERS_MAP = {
#     NewsProvider.REDDIT: provider_reddit_news,
#     NewsProvider.API_SECURITY: provider_api_security_news
# }
#
# FORCE_PROCESS_FEEDS = decouple.config("FORCE_PROCESS_FEEDS", default=False, cast=bool)
#
#
# # -------------------------------------------------------------------------
# # Auxiliar functions
# # -------------------------------------------------------------------------
# def parse_news(event: dict) -> Iterable[News]:
#     for item in event.get("items", []):
#         yield News.from_json(item)
#
#
# @shared_task(name="inoreader_distributor")
# def inoreader_distributor(webhook_content: dict):
#     #
#     # En el body se espera un JSON con la estructura inoreader.json
#     #
#     try:
#         print("[*] Processing InoReader feed", flush=True)
#         feed = InoReader.from_json(webhook_content)
#
#         if not FORCE_PROCESS_FEEDS and feed.matches_today < 1:
#             print("[!] No matches today", flush=True)
#             return
#
#         #
#         # Process each feed item
#         #
#         for news in parse_news(webhook_content):
#             print(f"[*] Processing news: {news.title}")
#
#             try:
#                 fn = PROVIDERS_MAP[news.provider]
#             except KeyError:
#                 raise ValueError(f"Invalid provider: {news.provider}")
#
#             for c in fn(news):
#                 # Publish to Notion
#                 print(f"[*] Publishing to Notion: {c.title}")
#                 publish_to_notion(c)
#
#                 # Add the news to the database
#                 print(f"[*] Adding to the database: {c.title}")
#
#     except Exception as e:
#         notify_pushover("Error processing InoReader feed", str(e))
#     finally:
#         notify_pushover("Feed processed", "InoReader feed processed")
