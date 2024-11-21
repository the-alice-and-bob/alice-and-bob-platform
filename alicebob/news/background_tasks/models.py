from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from typing import List, Iterable, Tuple, Dict


class NewsTags(Enum):
    API = "API"
    SECURITY = "Security"
    HACKING = "Hacking"
    PYTHON = "Python"
    BREACH = "Breach"
    VULNERABILITY = "Vulnerability"
    ZERO_DAY = "ZeroDay"

    @staticmethod
    def tags() -> list:
        return [
            t.value
            for t in NewsTags
        ]

    @classmethod
    def from_str(cls, value: str) -> "NewsTags":
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid value: {value}")


class NewsProvider(Enum):
    REDDIT = 1
    API_SECURITY = 2

    @classmethod
    def from_str(cls, value: dict) -> "NewsProvider":
        feed = value.get("streamId", None)

        if "reddit.com" in feed:
            return cls.REDDIT

        elif "apisecurity.io" in feed:
            return cls.API_SECURITY

        else:
            raise ValueError(f"Invalid value: {value}")


@dataclass
class News:
    title: str
    summary: str
    origin: str
    published: datetime
    provider: NewsProvider

    @classmethod
    def from_json(cls, data: dict):
        published: int or None = data.get("published", None)

        if published is None:
            raise ValueError("Invalid published date")

        summary = data.get("summary", {}).get("content", "")

        if not summary:
            raise ValueError("Invalid summary content")

        return cls(
            title=data.get("title", ""),
            provider=NewsProvider.from_str(data.get("origin", {})),
            summary=summary,
            published=datetime.fromtimestamp(published),
            origin=data.get("origin", {}).get("htmlUrl", "")
        )


@dataclass
class InoReader:
    matches_today: int
    name: str

    @classmethod
    def from_json(cls, event: dict):
        try:
            matches_today = int(event.get("rule", {}).get("matchesToday", 0))
        except (ValueError, TypeError):
            matches_today = 0

        return cls(
            matches_today=matches_today,
            name=event.get("rule", {}).get("name", "")
        )


@dataclass
class SummarizedNews:
    title: str
    linkedin: str
    twitter: str
    tags: List[NewsTags]
    url: str
    published: datetime
    origin: str
    provider: str


__all__ = ("NewsTags", "NewsProvider", "News", "InoReader", "SummarizedNews")
