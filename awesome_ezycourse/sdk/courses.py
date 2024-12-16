from enum import Enum
from datetime import datetime
from typing import List, Iterable, Tuple, Optional
from dataclasses import dataclass, field

import requests

from .auth import Auth
from .utils.api import iterate_endpoint


class CourseException(Exception):
    ...


class CourseType(Enum):
    BUNDLE = "BUNDLE"
    SINGLE = "SINGLE"


class CourseStatus(Enum):
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"


class LessonType(Enum):
    VIDEO = "VIDEO"
    TEXT = "TEXT"
    QUIZ = "QUIZ"
    ASSIGNMENT = "ASSIGNMENT"

    @classmethod
    def from_text(cls, text) -> "LessonType":
        lesson_types = {
            "VIDEO": LessonType.VIDEO,
            "TEXT": LessonType.TEXT,
            "QUIZ": LessonType.QUIZ,
            "ASSIGNMENT": LessonType.ASSIGNMENT,
        }
        return lesson_types.get(text, LessonType.TEXT)


class PaymentGateway(Enum):
    STRIPE = "STRIPE"
    MANUAL = "MANUAL"
    COINS = "COINS"
    FREE = "FREE"


@dataclass
class CourseUserStatistics:
    """
    This class represents the statistics of a course.
    """
    status: str
    course_completion_date: datetime
    certificate_url: str
    certificate_id: str
    is_manual: bool
    start_date: datetime
    last_access: datetime
    student: "User"
    lessons_completed: int
    progress: int

    @classmethod
    def from_json(cls, json_data: dict) -> "CourseUserStatistics":
        """
        Json data example:

        {
          "id": 822185,
          "course_or_bundle_id": 13232,
          "bundle_enrollment_id": null,
          "user_id": 710217,
          "school_id": 794,
          "created_at": "2024-10-10T16:39:05.000+00:00",
          "updated_at": "2024-10-10T16:39:05.000+00:00",
          "expire_date": null,
          "status": "ACTIVE",
          "pause_date": null,
          "order_id": 268563,
          "course_completion_date": null,
          "certificate_url": null,
          "certificate_id": null,
          "is_manual": 0,
          "plan_id": null,
          "custom_certificate_id": null,
          "start_date": null,
          "last_visit_in": null,
          "seller_id": null,
          "ref_community_id": null,
          "student": {
            "id": 710217,
            "email": "xxx@xx.com",
            "full_name": "xxxx",
            "meta": { }
          },
          "order": {
            "subscription_status": "ACTIVE",
            "gateway": "STRIPE",
            "id": 268563,
            "meta": { }
          },
          "meta": {
            "charge_option": null,
            "later_charge_date": null,
            "lessons_count": 13,
            "progress_count": 0
          }
        }
        """

        from .users import User

        try:
            start_date = datetime.strptime(json_data["start_date"], "%Y-%m-%dT%H:%M:%S.%f%z")
        except (ValueError, TypeError):
            start_date = None

        try:
            last_visit_in = datetime.strptime(json_data["last_visit_in"], "%Y-%m-%dT%H:%M:%S.%f%z")
        except (ValueError, TypeError):
            last_visit_in = None

        try:
            course_completion_date = datetime.strptime(json_data["course_completion_date"], "%Y-%m-%dT%H:%M:%S.%f%z")
        except (ValueError, TypeError):
            course_completion_date = None

        student = User(
            identifier=json_data["student"]["id"],
            email=json_data["student"]["email"],
            full_name=json_data["student"]["full_name"],
        )

        return cls(
            status=json_data["status"],
            course_completion_date=course_completion_date,
            certificate_url=json_data["certificate_url"],
            certificate_id=json_data["certificate_id"],
            is_manual=json_data["is_manual"],
            start_date=start_date,
            last_access=last_visit_in,
            student=student,
            lessons_completed=json_data["meta"]["lessons_count"],
            progress=json_data["meta"]["progress_count"],
        )


@dataclass
class CourseStatistics:
    total_instructors: int
    total_categories: int
    total_lessons: int
    total_reviews: int
    total_orders: int
    total_amount: int
    total_enrollments: int

    @classmethod
    def from_list_json(cls, json_data: dict) -> "CourseStatistics":
        return cls(
            total_instructors=json_data["total_instructors"],
            total_categories=json_data["total_categories"],
            total_lessons=json_data["total_lessons"],
            total_reviews=json_data["total_reviews"],
            total_orders=json_data["total_orders"],
            total_amount=json_data["total_amount"],
            total_enrollments=json_data["total_enrollments"],
        )


@dataclass
class CourseLesson:
    identifier: int
    title: str
    position: int
    published: CourseStatus
    lesson_type: LessonType
    is_free: bool

    @classmethod
    def from_json(cls, json_data: dict) -> "CourseLesson":
        if json_data["is_published"] == "PUBLISHED":
            published = CourseStatus.PUBLISHED
        else:
            published = CourseStatus.DRAFT

        return cls(
            identifier=json_data["id"],
            title=json_data["title"],
            position=json_data["position"],
            published=published,
            is_free=True if json_data["is_free"] == "1" else False,
            lesson_type=LessonType.from_text(json_data["lesson_type"])
        )


@dataclass
class CourseChapter:
    identifier: int
    title: str
    position: int
    content: str
    published: CourseStatus
    lessons: List[CourseLesson]

    @classmethod
    def from_json(cls, json_data: dict) -> "CourseChapter":
        if json_data["is_published"] == "PUBLISHED":
            published = CourseStatus.PUBLISHED
        else:
            published = CourseStatus.DRAFT

        return cls(
            identifier=json_data["id"],
            title=json_data["title"],
            position=json_data["position"],
            published=published,
            content=json_data["content"],
            lessons=[CourseLesson.from_json(lesson) for lesson in json_data.get("lessons", [])]
        )


@dataclass
class Enrollment:
    student: "User"
    status: str
    order_id: int
    is_manual: bool
    start_date: datetime  # Day when the user started the course
    last_visit: datetime  # Last time the user accessed the course
    identifier: int
    updated: datetime
    created: datetime
    gateway: Optional[PaymentGateway] = None
    progress: int | None = None
    course_completion_date: datetime | None = None

    # This is a flag to know if the user has paid for the course
    user_paid_course: bool = False


@dataclass
class Course:
    auth: Auth

    identifier: str
    title: str
    image: str
    is_published: CourseStatus
    course_type: CourseType
    course_slug: str
    approval_status: str

    price: float | None = None
    content: str | None = None
    published_date: datetime | None = None
    short_description: str | None = None
    language: str | None = None
    chapters: List[CourseChapter] = field(default_factory=list)

    URL_COURSE_STATISTICS = "/api/teacher/course/getAllEnrolled"

    def get_statistics(self) -> Iterable[CourseUserStatistics]:
        query_params = {
            "str": None,
            "page": 1,
            "pageSize": 50,
        }

        headers = self.auth.get_headers()

        target_url = f"{self.auth.site}{self.URL_COURSE_STATISTICS}/{self.identifier}"

        response = requests.get(
            target_url,
            params=query_params,
            headers=headers,
        )

        if response.status_code != 200:
            raise CourseException(f"Failed to get course statistics: {response.text}")

        data = response.json()

        # Return the first page
        yield from [CourseUserStatistics.from_json(user) for user in data.get("data", [])]

        # Get total last page
        last_page = data["meta"]["last_page"]

        # If there are more pages, get them
        if last_page > 1:
            for page in range(2, last_page + 1):
                query_params["page"] = page

                response = requests.get(
                    target_url,
                    params=query_params,
                    headers=headers,
                )

                if response.status_code != 200:
                    raise CourseException(f"Failed to get course statistics: {response.text}")

                data = response.json()

                yield from [CourseUserStatistics.from_json(user) for user in data.get("data", [])]

    def get_enrolled(self) -> Iterable[Enrollment]:
        from .users import User

        url_enrolled = "/api/teacher/course/getAllEnrolled/"
        query_params = {
            "str": None,
            "page": 1,
            "pageSize": 50,
        }
        url = f"{self.auth.site}{url_enrolled}/{self.identifier}"
        headers = self.auth.get_headers()

        for users_data in iterate_endpoint(url, "get", headers, query_params):

            for v in users_data.get("data", []):
                """
                API JSON response example for PAID users:
                
                {
                  "id": 822185,
                  "course_or_bundle_id": 13232,
                  "bundle_enrollment_id": null,
                  "user_id": 710217,
                  "school_id": 794,
                  "created_at": "2024-10-10T16:39:05.000+00:00",
                  "updated_at": "2024-10-10T16:39:05.000+00:00",
                  "expire_date": null,
                  "status": "ACTIVE",
                  "pause_date": null,
                  "order_id": 268563,
                  "course_completion_date": null,
                  "certificate_url": null,
                  "certificate_id": null,
                  "is_manual": 0,
                  "plan_id": null,
                  "custom_certificate_id": null,
                  "start_date": null,
                  "last_visit_in": null,
                  "seller_id": null,
                  "ref_community_id": null,
                  "student": {
                    "id": 710217,
                    "email": "alicebob@rodriguezvazquez.com",
                    "full_name": "Fernando Rodríguez",
                    "meta": { }
                  },
                  "order": {
                    "subscription_status": "ACTIVE",
                    "gateway": "STRIPE",
                    "id": 268563,
                    "meta": { }
                  },
                  "meta": {
                    "charge_option": null,
                    "later_charge_date": null,
                    "lessons_count": 13,
                    "progress_count": 0
                  }
                }
                """

                """
                Example for FREE users:
                
                {
                    "meta":
                        {
                            "total": 587,
                            "per_page": 10,
                            "current_page": 1,
                            "last_page": 59,
                            "first_page": 1,
                            "first_page_url": "/?page=1",
                            "last_page_url": "/?page=59",
                            "next_page_url": "/?page=2",
                            "previous_page_url": null
                        },
                        "data":
                        [
                            {
                                "id": 439093,
                                "course_or_bundle_id": 10978,
                                "bundle_enrollment_id": null,
                                "user_id": 697843,
                                "school_id": 794,
                                "created_at": "2024-07-30T07:43:10.000+00:00",
                                "updated_at": "2024-07-30T07:43:10.000+00:00",
                                "expire_date": null,
                                "status": "ACTIVE",
                                "pause_date": null,
                                "order_id": 194294,
                                "course_completion_date": null,
                                "certificate_url": null,
                                "certificate_id": null,
                                "is_manual": 0,
                                "plan_id": null,
                                "custom_certificate_id": null,
                                "start_date": null,
                                "last_visit_in": null,
                                "seller_id": null,
                                "ref_community_id": null,
                                "order":
                                {
                                    "subscription_status": "ACTIVE",
                                    "gateway": "FREE",
                                    "id": 194294,
                                    "meta":
                                    {}
                                },
                                "student":
                                {
                                    "id": 697843,
                                    "full_name": "Antonio  Moreno ",
                                    "meta":
                                    {},
                                    "email": "netmiyerapub@gmail.com"
                                },
                                "meta":
                                {
                                    "charge_option": null,
                                    "later_charge_date": null,
                                    "lessons_count": 19,
                                    "progress_count": 0
                                }
                            }
                        ]
                }
                """

                # Be careful with null dates
                try:
                    start_date = datetime.strptime(v["start_date"], "%Y-%m-%dT%H:%M:%S.%f%z")
                except:
                    start_date = None

                try:
                    last_visit_in = datetime.strptime(v["last_visit_in"], "%Y-%m-%dT%H:%M:%S.%f%z")
                except:
                    last_visit_in = None

                try:
                    updated = datetime.strptime(v["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                except:
                    updated = None

                try:
                    created = datetime.strptime(v["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                except:
                    created = None

                try:
                    course_completion_date = datetime.strptime(v["course_completion_date"], "%Y-%m-%dT%H:%M:%S.%f%z")
                except:
                    course_completion_date = None

                # Check if the user paid for the course
                if v["order"]["gateway"] in (PaymentGateway.FREE.value, PaymentGateway.MANUAL.value):
                    user_paid_course = False
                else:
                    user_paid_course = True

                yield Enrollment(
                    student=User(
                        identifier=v["student"]["id"],
                        email=v["student"]["email"],
                        full_name=v["student"]["full_name"]
                    ),
                    gateway=PaymentGateway(v.get("order", {}).get("gateway", None)),
                    status=v["status"],
                    order_id=v["order_id"],
                    is_manual=v["is_manual"],
                    start_date=start_date,
                    last_visit=last_visit_in,
                    identifier=v["id"],
                    updated=updated,
                    created=created,
                    progress=v.get("meta", {}).get("progress_count", 0),
                    course_completion_date=course_completion_date,
                    user_paid_course=user_paid_course
                )

    def __repr__(self):
        return f"<Course(title={self.title}, identifier={self.identifier})>"

    def __str__(self):
        return f"{self.title} ({self.identifier})"


class Courses:
    API_LIST_URL = "/api/teacher/course/getAllCourses"
    API_GET_URL = "/api/public/course/singe-course-details-with-metadata/"

    def __init__(self, auth: Auth):
        self.auth = auth

    def get(self, course_id: str | int) -> Course:
        """
        API response example:

        {
          "id": 13935,
          "title": "Todos los cursos de Alice & Bob de 2024",
          "content": "<h1 id=\"3dadaf1d-4d31-48a9-8a54-fd3a1528089f\" data-toc-id=\"3dadaf1d-4d31-48a9-8a54-fd3a1528089f\">Todos los cursos 2024</h1><p>Todos los cursos de Alice &amp; Bob a un precio genial.</p><p>Incluyendo todos los cursos que se <strong>publiquen en 2024.</strong></p><p>Cualquier curso que se publique durante 2024 se añadirán a la lista de cursos. <strong>Sin pagar un céntimo más.</strong></p><p></p><p></p>",
          "image": "https://letcheck.b-cdn.net/794/all-2024-1728997679483.png",
          "cover_image": null,
          "course_slug": "todos-los-cursos-de-alice-and-bob-2024",
          "creator_id": 2609,
          "school_id": 794,
          "course_type": "BUNDLE",
          "pricing_type": "FREE",
          "course_category": null,
          "published_date": null,
          "short_description": "Todos los cursos de 2024 con un descuento",
          "is_published": "PUBLISHED",
          "presell_charge_option": null,
          "enrollment_count_hidden": 1,
          "landing_page": null,
          "preview_video_meta": null,
          "course_preview_type": "IMAGE",
          "course_includes_list": [
            "Disfrutar en App móvil y TV",
            "Acceso de por vida",
            "Recursos descargables",
            "Referencias esenciales",
            "+8 horas de video"
          ],
          "course_learning_list": null,
          "guarantee_text": null,
          "course_level": null,
          "course_faq": null,
          "course_language": "Español",
          "video_duration": null,
          "approval_status": null,
          "progressive_mode": 0,
          "enable_course_review": 1,
          "total_reviews": null,
          "avg_review": null,
          "landing_template_id": 1,
          "categories_names": [ ],
          "custom_course_page": null,
          "chapter": [ ],
          "prices": [
            {
              "id": 128395,
              "currency": "EUR",
              "price": 550,
              "strike_through_price": 0,
              "price_type": "ONE_TIME",
              "interval": null,
              "interval_count": 1,
              "trial_period_days": 0,
              "tier_type": null,
              "tiers": null,
              "enrollment_days": null,
              "is_default": 1,
              "total_installments": null,
              "without_card_enable": 0,
              "course_id": 13935,
              "meta": { }
            }
          ],
          "user": {
            "id": 2609,
            "full_name": "Daniel Garcia",
            "profile_pic": "https://letcheck.b-cdn.net/794/clx8skilr004n0z8zh36x2ltg.jpg",
            "meta": { }
          },
          "enrolled": null,
          "course_instructors": [ ],
          "videoHours": null,
          "bundle_courses": [
            {
              "id": 8058,
              "title": "101 - Primeros pasos en diseño de protocolos con Python y Scapy",
              "image": "https://letcheck.b-cdn.net/794/clyh9yp6501vze08z5pw35uar.png",
              "created_at": "2024-04-10T13:09:02.000+00:00",
              "short_description": "Para correr hay que empezar caminando.\n\nSi te cuentan otra cosa es un milonga.\n\nAprende la base sobre protocolos y Scapy para crear y manipular protocolos de comunicaciones.",
              "updated_at": "2024-09-28T19:46:47.000+00:00",
              "course_slug": "primeros-pasos-en-diseño-de-protocolos-con-python-y-scapy",
              "landing_page": null,
              "custom_course_page": null,
              "meta": {
                "pivot_bundle_id": 13935,
                "pivot_course_id": 8058
              }
            },
            {
              "id": 12602,
              "title": "101 - Introducción seguridad APIs REST",
              "image": "https://letcheck.b-cdn.net/794/cover-1725532786871.png",
              "created_at": "2024-09-05T10:47:23.000+00:00",
              "short_description": "Este curso te dará las nociones esenciales para entender cómo afrontar la seguridad de las APIs REST",
              "updated_at": "2024-10-10T09:06:20.000+00:00",
              "course_slug": "introduccion-seguridad-apis-rest",
              "landing_page": null,
              "custom_course_page": null,
              "meta": {
                "pivot_bundle_id": 13935,
                "pivot_course_id": 12602
              }
            },
            {
              "id": 10978,
              "title": "301 - Ocultación y ejecución de código Python",
              "image": "https://letcheck.b-cdn.net/794/clz6m5qfk00os4q9n6bcb4bkx.png",
              "created_at": "2024-07-29T06:27:15.000+00:00",
              "short_description": "Este curso se mete de lleno en las artes, un poco turbias, de cómo esconder y ejecutar código Python. Aprenderás trucos para que tu código pase desapercibido, ya sea para ojos curiosos o para esos molestos analizadores de código.",
              "updated_at": "2024-09-28T19:36:58.000+00:00",
              "course_slug": "301-ocultacion-y-ejecucion-de-codigo-python",
              "landing_page": null,
              "custom_course_page": null,
              "meta": {
                "pivot_bundle_id": 13935,
                "pivot_course_id": 10978
              }
            },
            {
              "id": 13232,
              "title": "102 - API Security Checklist",
              "image": "https://letcheck.b-cdn.net/794/cover-1727185494012.png",
              "created_at": "2024-09-24T13:39:38.000+00:00",
              "short_description": "En este curso explicaremos punto por punto la Security CheckList más completa para APIs REST",
              "updated_at": "2024-10-10T13:18:21.000+00:00",
              "course_slug": "102-api-security-checklist",
              "landing_page": null,
              "custom_course_page": null,
              "meta": {
                "pivot_bundle_id": 13935,
                "pivot_course_id": 13232
              }
            }
          ],
          "meta": {
            "videos_count": 0,
            "assingments_count": 0,
            "download_able_source_count": 0,
            "chapter_count": 0,
            "enrolled_count": 1,
            "lessons_count": 66,
            "quizes_count": 1
          }
        }
        """

        headers = self.auth.get_headers()

        target_url = f"{self.auth.site}{self.API_GET_URL}/{course_id}"

        response = requests.get(
            target_url,
            headers=headers,
        )

        if response.status_code != 200:
            raise CourseException(f"Failed to get course: {response.text}")

        try:
            data = response.json()
        except ValueError:
            raise CourseException("Invalid JSON response")

        try:
            published_date = datetime.strptime(data["published_date"], "%Y-%m-%dT%H:%M:%S.%f%z")
        except (ValueError, TypeError):
            published_date = None

        if "SINGLE" in data["course_type"]:
            course_type = CourseType.SINGLE
        else:
            course_type = CourseType.BUNDLE

        try:
            price = data["prices"][0]["price"]
        except (KeyError, IndexError):
            price = 0

        return Course(
            auth=self.auth,
            identifier=data["id"],
            price=price,
            title=data["title"],
            image=data["image"],
            is_published=data["is_published"],
            content=data["content"],
            course_type=course_type,
            language=data.get("course_language", None),
            published_date=published_date,
            short_description=data["short_description"],
            course_slug=data["course_slug"],
            approval_status=data["approval_status"],
            chapters=[CourseChapter.from_json(chapter) for chapter in data.get("chapter", [])]
        )

    def list_courses(self) -> Iterable[Tuple[Course, CourseStatistics]]:
        """

        The API response is a JSON object with the following structure:

        {
          "meta": {
            "total": 7,
            "per_page": 50,
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
              "id": 13935,
              "image": "https://letcheck.b-cdn.net/794/all-2024-1728997679483.png",
              "title": "Todos los cursos de Alice & Bob de 2024",
              "is_published": "PUBLISHED",
              "course_type": "BUNDLE",
              "created_at": "2024-10-15T12:32:13.000Z",
              "course_slug": "todos-los-cursos-de-alice-and-bob-2024",
              "approval_status": null,
              "list_on_ezycourse_status": 0,
              "total_instructors": 0,
              "total_categories": 0,
              "total_lessons": 0,
              "total_reviews": 0,
              "total_orders": 1,
              "total_amount": 550,
              "total_enrollments": 1
            }
          ]
        }
        """
        page = 1
        page_size = 50

        query_params = {
            "str": "",
            "type": "ALL",
            "status": "ALL",
            "teacher": "ALL",
            "category_id": "ALL",
            "order": "",
            "date1": "",
            "date2": "",
            "page": page,
            "pageSize": page_size,
        }

        headers = self.auth.get_headers()
        headers["Content-Type"] = "application/json"

        target_url = f"{self.auth.site}{self.API_LIST_URL}"

        response = requests.get(
            target_url,
            params=query_params,
            headers=headers,
        )

        if response.status_code != 200:
            raise CourseException(f"Failed to list courses: {response.text}")

        try:
            data = response.json()
        except ValueError:
            raise CourseException("Invalid JSON response")

        for course in data.get("data", []):
            if course["course_type"] == "BUNDLE":
                course_type = CourseType.BUNDLE
            else:
                course_type = CourseType.SINGLE

            if course["is_published"] == "PUBLISHED":
                published = CourseStatus.PUBLISHED
            else:
                published = CourseStatus.DRAFT

            course_obj = Course(
                auth=self.auth,
                identifier=course["id"],
                title=course["title"],
                image=course["image"],
                is_published=published,
                course_type=course_type,
                published_date=course["created_at"],
                course_slug=course["course_slug"],
                approval_status=course["approval_status"]
            )

            yield course_obj, CourseStatistics.from_list_json(course)

    def create(self, course: Course) -> Course:
        ...

    def update(self, course: Course) -> Course:
        ...

    def delete(self, course_id: str) -> None:
        ...
