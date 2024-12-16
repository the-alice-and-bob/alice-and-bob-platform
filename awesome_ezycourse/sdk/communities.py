"""
This file contains the implementation of the Communities class which is used to interact with the communities API.

The API documentation can be found at https://www.alicebob.io/api/communities
"""
import re
import json
import datetime

from enum import Enum
from time import sleep

from urllib.parse import urljoin
from typing import List, Iterable
from dataclasses import dataclass, field

import requests

from .auth import Auth
from .utils import extract_og

URL_PATTERN = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?')


class CommunityException(Exception):
    ...


class PricingTypes(Enum):
    FREE = 1
    PAID = 2


class CommunityPrivacy(Enum):
    PUBLIC = 1
    PRIVATE = 2
    MEMBERS_ONLY = 3


@dataclass
class CommunityPricing:
    price_type: str
    price: int
    interval: str
    interval_count: int
    community_id: int
    strike_through_price: str = None
    meta: dict = field(default_factory=dict)

    @classmethod
    def from_json(cls, data) -> "CommunityPricing":
        return cls(
            price_type=data["price_type"],
            price=data["price"],
            interval=data.get("interval", None),
            interval_count=data.get("interval_count", 0),
            community_id=data["community_id"],
            strike_through_price=data["strike_through_price"],
            meta=data["meta"],
        )


@dataclass
class CommunityPost:
    identifier: int
    user_id: int
    community_id: int
    content: str
    status: str
    slug: str
    title: str
    is_pinned: int
    file_type: str
    files: List[str]
    likes: int
    comment_count: int
    share_count: int

    created_at: datetime.datetime
    updated_at: datetime.datetime

    feed_privacy: str

    author_pic: str = None
    author_name: str = None
    author_id: int = None

    @classmethod
    def from_json(cls, data) -> "CommunityPost":
        """
        Load data from a JSON response.

        This is an example of the JSON response:

        {
            "id": 163934,
            "school_id": 794,
            "user_id": 2609,
            "course_id": null,
            "community_id": 1921,
            "group_id": null,
            "feed_txt": "\u00a1Estrenamos comunidad!\nSeguridad y otras yerbas\n\nhttps://www.alicebob.io/es/community/seguridad-y-otras-yerbas-2223",
            "status": "APPROVED",
            "slug": "estrenamos-comunidad-seguridad-y-otras-yerbas-httpswwwalicebobioescommunityseguridad-y-otras-yerbas-2223",
            "title": "Estrenamos comunidad Seguridad y otras yerbas httpswwwalicebobioescommunityseguridad-y-otras-yerbas-2223",
            "activity_type": "group",
            "is_pinned": 0,
            "file_type": "text",
            "files": [],
            "like_count": 1,
            "comment_count": 0,
            "share_count": 0,
            "share_id": 0,
            "meta_data": {
                "linkMeta": {
                    "title": "Seguridad y otras yerbas",
                    "image": "https://letcheck.b-cdn.net/794/clx376fnm091nst8zgeb588bx.png",
                    "url": "https://www.alicebob.io/es/community/seguridad-y-otras-yerbas-2223"
                }
            },
            "created_at": "2024-10-14T13:55:51.000Z",
            "updated_at": "2024-10-14T13:55:51.000+00:00",
            "feed_privacy": "Public",
            "is_background": 1,
            "bg_color": "{\"backgroundImage\":\"linear-gradient(45deg, rgb(255, 115, 0) 0%, rgb(255, 0, 234) 100%)\"}",
            "poll_id": null,
            "lesson_id": null,
            "space_id": 3656,
            "video_id": null,
            "stream_id": null,
            "blog_id": null,
            "schedule_date": null,
            "timezone": "Europe/Madrid",
            "is_anonymous": 0,
            "meeting_id": null,
            "seller_id": null,
            "publish_date": null,
            "is_feed_edit": false,
            "name": "Daniel Garcia",
            "pic": "https://letcheck.b-cdn.net/794/clx8skilr004n0z8zh36x2ltg.jpg",
            "uid": 2609,
            "is_private_chat": 0,
            "stream_details": null,
            "group": null,
            "likeType": [
                {
                    "reaction_type": "LIKE",
                    "feed_id": 163934,
                    "meta": {}
                }
            ],
            "user": {
                "id": 2609,
                "full_name": "Daniel Garcia",
                "profile_pic": "https://letcheck.b-cdn.net/794/clx8skilr004n0z8zh36x2ltg.jpg",
                "is_private_chat": 0,
                "expire_date": null,
                "status": null,
                "email": "xx@xx.com",
                "pause_date": null,
                "user_type": "SITE_OWNER",
                "meta": {}
            },
            "poll": null,
            "comments": [],
            "meta": {
                "views": 0,
                "gifted_coins": null
            }
        }
        """
        return cls(
            identifier=data["id"],
            user_id=data["user_id"],
            community_id=data["community_id"],
            content=data["feed_txt"],
            status=data["status"],
            slug=data["slug"],
            title=data["title"],
            is_pinned=data["is_pinned"],
            file_type=data["file_type"],
            files=data["files"],
            likes=data["like_count"],
            comment_count=data["comment_count"],
            share_count=data["share_count"],
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(data["updated_at"]),
            feed_privacy=data["feed_privacy"],

            author_pic=data["pic"],
            author_name=data["name"],
            author_id=data["uid"],
        )

    def __repr__(self):
        return f"<CommunityPost {self.title}>"

    def __str__(self):
        return self.title


@dataclass
class PostMetaLink:
    site_name: str
    title: str
    url: str
    image: str

    @classmethod
    def from_url(cls, url: str):
        og = extract_og(url)

        return cls(
            site_name=og.site_name,
            title=og.title,
            url=og.url,
            image=og.image
        )


@dataclass
class CommunitySpace:
    # Class constants
    LIST_POST_URL = "/api/public/feeds/{slug}&status=feed"
    CREATE_POST_URL = '/api/teacher/community/createFeed'

    # Class parameters
    identifier: int
    name: str
    is_admin_only: int

    created_at: datetime.datetime
    updated_at: datetime.datetime

    auth: "Auth"
    community: "Community"

    pricing_type: PricingTypes = field(default=PricingTypes.FREE)

    def create_post(self, content) -> int:
        """
        Request example:
        {
          "community_id": "demo-2404",
          "space_id": 4652,
          "isScheduled": false,
          "is_anonymous": false,
          "timezone": "Europe/Madrid",
          "schedule_date": null,
          "feed_txt": "Con un enlace\n\nHello world!!\n\nhttps://www.alicebob.io/es",
          "uploadType": "text",
          "poll_options": null,
          "poll_privacy": null,
          "meta_data": {
            "linkMeta": {
              "siteName": "Alice & Bob Learning",
              "title": "home",
              "url": "https://www.alicebob.io/es",
              "image": "https://letcheck.b-cdn.net/794/clx376fnm091nst8zgeb588bx.png"
            },
            "contentsMetaData": null
          },
          "feed_privacy": "PUBLIC",
          "activity_type": "group",
          "files": null,
          "is_background": 0,
          "bg_color": null,
          "ids": "[]"
        }
        """

        _url = urljoin(self.auth.site, self.CREATE_POST_URL)

        data = {
            "community_id": self.community.full_slug,
            "space_id": self.identifier,
            "isScheduled": False,
            "is_anonymous": False,
            "timezone": "Europe/Madrid",
            "schedule_date": None,
            "feed_txt": content,
            "uploadType": "text",
            "poll_options": None,
            "poll_privacy": None,
            "meta_data": {
                "linkMeta": None,
                "contentsMetaData": None
            },
            "feed_privacy": "PUBLIC",
            "activity_type": "group",
            "files": None,
            "is_background": 0,
            "bg_color": None,
            "ids": "[]"
        }

        # Try to extract the link from the content
        match = URL_PATTERN.search(content)
        if match:
            # Extract the link. Only the first one
            link = PostMetaLink.from_url(match.group(0))

            # Update the data
            data["meta_data"]["linkMeta"] = {
                "siteName": link.site_name,
                "title": link.title,
                "url": link.url,
                "image": link.image
            }

        headers = self.auth.get_headers()
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json, text/plain, */*"

        response = requests.post(_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json()["id"]

        else:
            raise CommunityException(f"Error creating post: {response.text}")

    def list_posts(self) -> Iterable[CommunityPost]:
        try:
            _url = urljoin(self.auth.site, self.LIST_POST_URL.format(slug=self.community.full_slug))

            _response = requests.get(_url, headers=self.auth.get_headers())

            for post in _response.json() or []:
                yield CommunityPost.from_json(post)

        except requests.exceptions.RequestException as e:
            raise CommunityException(f"Error fetching posts: {e}")

    # -------------------------------------------------------------------------
    # Alternative constructors
    # -------------------------------------------------------------------------
    @classmethod
    def from_json(cls, auth: "Auth", community: "Community", data: dict) -> "CommunitySpace":
        """
        Example of request:

        {
          "id": 4652,
          "name": "General",
          "community_id": 2404,
          "is_admin_only": 0,
          "pricing_type": null,
          "space_content": null,
          "school_id": 794,
          "creator_id": 2609,
          "created_at": "2024-10-28T10:16:57.000+00:00",
          "updated_at": "2024-10-28T10:16:57.000+00:00",
          "position": 0,
          "deleted_at": null,
          "is_seller": null,
          "isFollowing": {
            "id": 12898,
            "user_id": 2609,
            "item_id": 4652,
            "type": "space",
            "plan_id": null,
            "order_id": null,
            "created_at": "2024-10-28T10:16:57.000+00:00",
            "updated_at": "2024-10-28T10:16:57.000+00:00",
            "seller_id": null
          },
          "pricing": null,
          "user_has_notification": false
        }
        """
        return cls(
            auth=auth,
            community=community,
            identifier=data["id"],
            name=data["name"],
            is_admin_only=data["is_admin_only"],
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(data["updated_at"]),
            pricing_type=PricingTypes.FREE
        )


@dataclass
class CommunityMember:
    identifier: int
    is_online: bool
    full_name: str
    last_login: datetime.datetime
    profile_pic: str
    feeds_count: int


class Community:
    COMMUNITY_LIST_MEMBERS_URL = "/api/teacher/community/getMembersForCommunity/{}?str=&page=1&limit=10"
    CREATE_POST_URL = "/api/teacher/community/createFeed"
    SPACES_URL = "/api/public/communities/{community_id}/spaces"

    def __init__(
            self,
            auth: "Auth",
            identifier: int,
            title: str,
            about: str,
            short_description: str,
            cover: str,
            pricing_type: PricingTypes,
            slug: str,
            total_members: int,
            pricing: CommunityPricing,
    ):
        self.auth = auth
        self.identifier = identifier
        self.title = title
        self.cover = cover
        self.pricing_type = pricing_type
        self.slug = slug
        self.total_members = total_members
        self.pricing = pricing
        self.about = about
        self.short_description = short_description

    @property
    def url(self) -> str:
        """
        Return the URL of the community
        """
        return urljoin(self.auth.site, f"/community/{self.slug}-{self.identifier}")

    @property
    def full_slug(self) -> str:
        """
        Return the path of the community
        """
        return f"{self.slug}-{self.identifier}"

    def create_post(self, content):
        """
        Create a post in the community
        """

        data = {
            "community_id": "seguridad-y-otras-yerbas-2223",
            "space_id": 4458,
            "isScheduled": False,
            "is_anonymous": False,
            "timezone": "Europe/Madrid",
            "schedule_date": None,
            "feed_txt": content,
            "uploadType": "text",
            "poll_options": None,
            "poll_privacy": None,
            "meta_data": {
                "linkMeta": None,
                "contentsMetaData": None
            },
            "feed_privacy": "PUBLIC",
            "activity_type": "group",
            "files": None,
            "is_background": 0,
            "bg_color": None,
            "ids": "[]"
        }

        response = requests.post(self.CREATE_POST_URL, headers=self.auth.get_headers(), data=json.dumps(data))

        return response.json()

    def list_spaces(self) -> Iterable[CommunitySpace]:
        """
        List all spaces in the community
        """
        try:
            _url = urljoin(self.auth.site, self.SPACES_URL.format(community_id=self.identifier))

            _response = requests.get(_url, headers=self.auth.get_headers())

            for space in _response.json() or []:
                yield CommunitySpace.from_json(self.auth, self, space)

        except requests.exceptions.RequestException as e:
            raise CommunityException(f"Error fetching spaces: {e}")

    def get_space(self, space_id: int) -> CommunitySpace:
        """
        Get a space by its identifier
        """
        for space in self.list_spaces():
            if space.identifier == space_id:
                return space

        raise CommunityException(f"Space with id {space_id} not found")

    def list_members(self):
        try:
            _url = urljoin(self.auth.site, self.COMMUNITY_LIST_MEMBERS_URL.format(self.identifier))
            _response = requests.get(_url, headers=self.auth.get_headers())

            """
            Response example:
            [
                {
                    "id": 2609,
                    "is_online": "0",
                    "full_name": "Daniel Garcia",
                    "last_login": "2024-10-29T09:17:32.000+00:00",
                    "profile_pic": "https://letcheck.b-cdn.net/794/clx8skilr004n0z8zh36x2ltg.jpg",
                    "user_type": "SITE_OWNER",
                    "is_private_chat": 0,
                    "is_blocked_by_me": null,
                    "is_blocked_by_user": null,
                    "meta":
                    {
                        "feeds_count": 21
                    }
                }
            ]
            """

            data = _response.json()

            for member in data:
                if member.get("last_login"):
                    last_login = datetime.datetime.fromisoformat(member["last_login"])
                else:
                    last_login = None

                yield CommunityMember(
                    identifier=member["id"],
                    is_online=bool(int(member["is_online"])),
                    full_name=member["full_name"],
                    last_login=last_login,
                    profile_pic=member["profile_pic"],
                    feeds_count=member.get("meta", {}).get("feeds_count", 0)
                )

        except requests.exceptions.RequestException as e:
            raise CommunityException(f"Error fetching members: {e}")

    # -------------------------------------------------------------------------
    # Alternative constructors
    # -------------------------------------------------------------------------
    @classmethod
    def from_listed_json(cls, auth: "Auth", data) -> "Community":
        price_type = data["pricing_type"]

        if price_type == "FREE":
            price_type = PricingTypes.FREE

        elif price_type == "PAID":
            price_type = PricingTypes.PAID

        else:
            raise ValueError(f"Unknown price type: {price_type}")

        return cls(
            auth=auth,
            identifier=data["id"],
            title=data["title"],
            cover=data["cover"],
            pricing_type=price_type,
            slug=data["slug"],
            total_members=data["total_members"],
            pricing=data.get("pricing", {}).get("price", 0),
            about=None,
            short_description=None
        )

    @classmethod
    def from_by_id_json(cls, auth: "Auth", data) -> "Community":
        """
        Json example:

        {
          "id": 2404,
          "group_name": "demo",
          "short_description": "demo demo demo",
          "about": "<p>demo</p>",
          "profile_pic": "https://letcheck.b-cdn.net/794/comunidades-1728908539303.svg",
          "cover": "https://letcheck.b-cdn.net/794/comunidades-1728908539303.svg",
          "school_id": 794,
          "slug": "demo",
          "total_members": 1,
          "pricing": {
            "price_type": "FREE",
            "status": "ACTIVE",
            "community_id": 2404,
            "price": 0,
            "strike_through_price": null,
            "currency": "USD",
            "meta": { }
          },
          "is_members": null,
          "meta": {
            "total_feeds": 7
          }
        }
        """
        price_type = data["pricing"]["price_type"]

        if price_type == "FREE":
            price_type = PricingTypes.FREE

        elif price_type == "PAID":
            price_type = PricingTypes.PAID

        else:
            raise ValueError(f"Unknown price type: {price_type}")

        return cls(
            auth=auth,
            identifier=data["id"],
            title=data["group_name"],
            cover=data["cover"],
            pricing_type=price_type,
            slug=data["slug"],
            total_members=data["total_members"],
            pricing=CommunityPricing.from_json(data["pricing"]),
            about=data["about"],
            short_description=data["short_description"]
        )

    def __repr__(self):
        return f"<Community {self.title}>"

    def __str__(self):
        return self.title


class Communities:
    URL_LIST = "/api/public/communities"
    URL_GET_COMMUNITY = "/api/public/communities/get-by-id/{community_id}"

    def __init__(self, auth: "Auth"):
        self.auth = auth

    def list(self) -> List[Community]:
        """
        List all communities

        This is the API raw response:

        {
            "meta": {
                "total": 3,
                "per_page": 3,
                "current_page": 1,
                "last_page": 1,
                "first_page": 1,
                "first_page_url": "/?page=1",
                "last_page_url": "/?page=1",
                "next_page_url": null,
                "previous_page_url": null
            },
            "data": [
                {
                    "id": 2223,
                    "title": "Seguridad y otras yerbas",
                    "cover": "https://letcheck.b-cdn.net/794/comunidad-seguridad-1728903963067.png",
                    "pricing_type": "FREE",
                    "slug": "seguridad-y-otras-yerbas",
                    "total_members": 6,
                    "pricing": {
                        "price_type": "FREE",
                        "strike_through_price": null,
                        "price": 0,
                        "interval": null,
                        "interval_count": 1,
                        "community_id": 2223,
                        "meta": {}
                    },
                    "meta": {
                        "thumbnail": "https://letcheck.b-cdn.net/794/icon-1728904566055.png",
                        "total_feeds": 10
                    }
                },
                {
                    "id": 1993,
                    "title": "Comunidad Privada de API Security",
                    "cover": "https://letcheck.b-cdn.net/794/api-security-banner-1725958673978.png",
                    "pricing_type": "FREE",
                    "slug": "comunidad-privada-de-api-security",
                    "total_members": 2,
                    "pricing": {
                        "price_type": "FREE",
                        "strike_through_price": null,
                        "price": 0,
                        "interval": null,
                        "interval_count": 1,
                        "community_id": 1993,
                        "meta": {}
                    },
                    "meta": {
                        "thumbnail": "https://letcheck.b-cdn.net/794/api-security-icon-1725958854800.png",
                        "total_feeds": 1
                    }
                },
                {
                    "id": 1921,
                    "title": "Alice & Bob Noticias & Dudas",
                    "cover": "https://letcheck.b-cdn.net/794/general-bw-1724319181204.png",
                    "pricing_type": "FREE",
                    "slug": "alice-and-bob-noticias-and-dudas",
                    "total_members": 3,
                    "pricing": {
                        "price_type": "FREE",
                        "strike_through_price": null,
                        "price": 0,
                        "interval": null,
                        "interval_count": 1,
                        "community_id": 1921,
                        "meta": {}
                    },
                    "meta": {
                        "thumbnail": "https://letcheck.b-cdn.net/794/letras-1724311513947.png",
                        "total_feeds": 2
                    }
                }
            ]
        }
        """
        response = requests.get(urljoin(self.auth.site, self.URL_LIST), headers=self.auth.get_headers())

        return [
            Community.from_listed_json(
                self.auth,
                community_data
            )
            for community_data in response.json().get("data", [])
        ]

    def get(self, community_id: int) -> Community:
        """
        Get a community by its identifier
        """
        try:
            response = requests.get(
                urljoin(self.auth.site, self.URL_GET_COMMUNITY.format(community_id=community_id)), headers=self.auth.get_headers()
            )
        except requests.exceptions.RequestException as e:
            raise CommunityException(f"Error fetching community: {e}")

        if response.status_code == 200:
            return Community.from_by_id_json(self.auth, response.json())

        else:
            raise CommunityException(f"Community with id {community_id} not found")


__all__ = (
    "Communities", "Community", "CommunitySpace", "CommunityPricing", "CommunityPrivacy", "PricingTypes", "CommunityException",
    "CommunityMember", "CommunityPost", "PostMetaLink"
)

if __name__ == "__main__":

    # This is the cookie content of a response from server:
    # Set-Cookie: swuid=s%3AeyJtZXNzYWdlIjoiY20yMDZzdzdtMDBvc3dyOHpld2szMTFoMyIsInB1cnBvc2UiOiJzd3VpZCJ9.zCkRsWnl4TYvWH21ccxUqwzGQ4TxD1A-aNRO--kLPNk; Max-Age=5184000; Path=/; HttpOnly; Secure

    # I want to add to the request

    headers = {
        "Cookie": "swuid=s%3AeyJtZXNzYWdlIjoiY20yMDZzdzdtMDBvc3dyOHpld2szMTFoMyIsInB1cnBvc2UiOiJzd3VpZCJ9.zCkRsWnl4TYvWH21ccxUqwzGQ4TxD1A-aNRO--kLPNk"
    }

    # req = requests.get("https://www.alicebob.io/api/public/feeds/demo-2404&status=feed", headers=headers)
    # print(req.json())
    communities = Communities(site="https://www.alicebob.io")

    for c in communities.list():

        for p in c.list_post():
            print(p)
            sleep(0.1)

# for i in range(4000):
#     url = f"https://www.alicebob.io/api/public/feeds/seguridad-y-otras-yerbas-2223?space_id={i}&status=feed"
#
#     response = requests.get(url)
#     try:
#         response = response.json()
#     except:
#         print(response.headers)
#         break
#
#     if response:
#         print(url)
#         print(response)
#         print("#" * 100)
