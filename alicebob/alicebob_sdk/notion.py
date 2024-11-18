from datetime import datetime

import decouple

from notion_client import Client

from alicebob.alicebob_sdk import SummarizedNews, News

NOTION_TOKEN = decouple.config("NOTION_TOKEN")
NOTION_DATABASE_ID = decouple.config("NOTION_DATABASE_ID")


def publish_to_notion(news: SummarizedNews):
    notion = Client(auth=NOTION_TOKEN)

    try:
        # body_content = (
        #     {
        #         "object": "block",
        #         "type": "paragraph",
        #         "paragraph": {
        #             "rich_text": [
        #                 {
        #                     "type": "text",
        #                     "text": {
        #                         "content": c
        #                     }
        #                 }
        #             ]
        #         }
        #     }
        #
        #     for c in news.original_content.split("\n")
        # )

        # Crear la página con propiedades
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Título": {"title": [{"text": {"content": news.title}}]},
                "Linkedin": {"rich_text": [{"text": {"content": news.linkedin}}]},
                "Twitter": {"rich_text": [{"text": {"content": news.twitter}}]},

                # Multi-select
                "Tags": {"multi_select": [
                    {"name": t.value}
                    for t in news.tags
                ]},

                "URL": {"url": news.url},

                "Estado de Publicación": {"select": {"name": "Backlog"}},

                "Proveedor": {"select": {"name": news.provider}},

                "Origen": {"select": {"name": news.origin}},

                # Fecha
                "Fecha Noticia": {"date": {"start": news.published.strftime("%Y-%m-%d")}},

                "Fecha de Publicación": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
            }
        )
    except Exception as e:
        raise ValueError(str(e))


def search_notion_database(origin: str, proveedor: str, titulo: str) -> int:
    """
    This function searches for a specific entry in a Notion database using the URL, provider, and title and returns the
    number of entries found.
    """
    notion = Client(auth=NOTION_TOKEN)

    filters = {
        "filter": {
            "and": [
                {
                    "property": "Origen",
                    "select": {
                        "equals": origin
                    }
                },
                {
                    "property": "Proveedor",
                    "select": {
                        "equals": proveedor
                    }
                },
                {
                    "property": "Título",
                    "title": {
                        "equals": titulo
                    }
                }
            ]
        }
    }

    response = notion.databases.query(database_id=NOTION_DATABASE_ID, **filters)
    return len(response.get("results", []))


def find_news(news: News) -> int:
    """
    Search for news in a Notion database using the URL, provider, and title of the news.

    Returns the number of entries found.
    """
    return search_notion_database(
        origin=news.origin,
        proveedor=news.provider.name.lower(),
        titulo=news.title
    )


if __name__ == '__main__':
    # Search in a notion database
    found = search_notion_database(
        url="https://danaepp.com/attacking-apis-using-json-injection",
        proveedor="Reddit - /r/netsec",
        titulo="Attacking APIs using JSON Injection"
    )

    print(found)

__all__ = ("publish_to_notion", "search_notion_database", "find_news")
