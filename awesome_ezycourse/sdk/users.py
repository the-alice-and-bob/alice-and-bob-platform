import random

from enum import Enum
from time import sleep
from typing import Iterable, Tuple, List, Set
from datetime import datetime
from dataclasses import dataclass

from .auth import Auth

from .courses import Courses
from .utils import iterate_endpoint


class UserType(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class UserEnrollmentStatus(Enum):
    ALL = "ALL"
    ENROLLED = "ENROLLED"


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"


@dataclass
class User:
    email: str
    identifier: int
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime | None = None
    last_login: datetime | None = None

    user_type: UserType = UserType.STUDENT

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def __repr__(self):
        return f"<User {self.identifier} - {self.full_name} ({self.email})>"


class Users:
    URL_LIST_USERS = "/api/teacher/student/getAllStudent"

    def __init__(self, auth: Auth):
        self.auth = auth

    def get_users(
            self,
            max_users: int | None = None,
            only_students: bool = True,
            enrolled_in_course: int | str | None = None,
            enrollment_status: UserEnrollmentStatus = UserEnrollmentStatus.ALL,
            sleep_time: int | str = "random",
            show_progress: bool = False
    ) -> Iterable[User]:
        """
        Get all users from the platform

        :param max_users: Maximum number of users to export
        :param show_progress: Show progress of the export
        :param only_students: Export only students, not teachers or admins
        :param enrollment_status: Filter users by enrollment status
        :param enrolled_in_course: Filter users by courses they are enrolled in
        :param sleep_time: Time to sleep between requests
        """

        """
        HTTP Response:
        
        {
          "meta": {
            "total": 753,
            "per_page": 10,
            "current_page": 2,
            "last_page": 76,
            "first_page": 1,
            "first_page_url": "/?page=1",
            "last_page_url": "/?page=76",
            "next_page_url": "/?page=3",
            "previous_page_url": "/?page=1"
          },
          "data": [
            {
              "id": 830280,
              "email": "xxxx@gmail.com",
              "school_id": 794,
              "can_write_doc": 0,
              "full_name": "xxx",
              "is_verified": "VERIFIED",
              "is_approved": 1,
              "user_type": "STUDENT",
              "created_at": "2024-10-15T07:05:48.000+00:00",
              "is_private_chat": 0,
              "updated_at": "2024-10-31T11:53:43.000+00:00",
              "profile_pic": "https://letcheck.b-cdn.net/human_icon.png",
              "is_online": "0",
              "bio": null,
              "user_id": null,
              "social_auth_provider": null,
              "last_login": "2024-10-31T11:53:43.000+00:00",
              "status": null,
              "is_suspended": 0,
              "pause_date": null,
              "expire_date": null,
              "last_name": "Merino",
              "order_id": null,
              "first_name": "Jose Miguel",
              "custom_fields": null,
              "is_allow_chat": null,
              "ref_id": null,
              "ref_commission_level_1": 0,
              "ref_is_cookie_destroy_after_checkout": 0,
              "ref_commission_level_2": 0,
              "parent_ref_id": null,
              "ref_com_l1_value_type": "percentage",
              "ref_com_l2_value_type": "percentage",
              "ref_allow_linked_membership": 0,
              "is_manual": 0,
              "referred_by": null,
              "is_eligible_for_special_offer": 0,
              "is_founding": null,
              "plan_id": null,
              "is_2fa_enabled": 0,
              "is_force_logout_enabled": 0,
              "payout_paypal_email": null,
              "ref_phy_commission_level_1": 0,
              "is_manual_private_chat": 0,
              "ref_phy_com_l1_value_type": "percentage",
              "site_owner_user_id": null,
              "ezy_affiliate_user_id": null,
              "stripe_payout_enabled": 0,
              "signup_method": "From Checkout of 102 - API Security Checklist(course)",
              "deleted_at": null,
              "signup_custom_fields_responses": null,
              "deleted_by": null,
              "ref_phy_commission_level_2": 0,
              "ref_phy_com_l2_value_type": "percentage",
              "total_noti_count": 7,
              "total_chat_noti_count": 0,
              "about_me": null,
              "total_sell": "0",
              "seller_unique_name": null,
              "globe_link": null,
              "youtube_link": null,
              "linkedin_link": null,
              "facebook_link": null,
              "seller_title": null,
              "cover_pic": null,
              "usersTags": [ ],
              "meta": {
                "accessToken": null,
                "created_by": null,
                "is_enrolled": 1,
                "organizer_id": null,
                "private_chat_owner_seller_id": null,
                "is_private_chat_from_seller": 0
              }
            }
          ]
        }
        """

        query_params = {
            "status": enrollment_status.value,
            "page": 1,
            "pageSize": 50,
            "zone": -1,
            "selfDelete": "ACTIVE"
        }

        if enrolled_in_course:
            query_params["courseID"] = enrolled_in_course

        url = f"{self.auth.site}{self.URL_LIST_USERS}"

        exported_users = 0
        max_users = max_users or float("inf")

        for data in iterate_endpoint(
                url=url,
                method="GET",
                headers=self.auth.get_headers(),
                query_params=query_params
        ):
            for user_data in data.get("data", []):

                if exported_users >= max_users:
                    return

                # Determine user type (student, teacher, admin)
                user_type = UserType.STUDENT if user_data["user_type"] == "STUDENT" else UserType.TEACHER

                if only_students and user_type != UserType.STUDENT:
                    continue

                # Determine user status
                if user_data["is_verified"] == "VERIFIED" and user_data["deleted_at"] is None:
                    user_state = UserStatus.ACTIVE
                elif user_data["deleted_at"] is not None:
                    user_state = UserStatus.DELETED
                else:
                    user_state = UserStatus.INACTIVE

                try:
                    last_login = datetime.strptime(user_data["last_login"], "%Y-%m-%dT%H:%M:%S.%f+00:00")
                except:
                    last_login = None

                yield User(
                    identifier=user_data["id"],
                    full_name=user_data["full_name"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    email=user_data["email"],
                    status=user_state,
                    user_type=user_type,
                    created_at=datetime.strptime(user_data["created_at"], "%Y-%m-%dT%H:%M:%S.%f+00:00"),
                    last_login=last_login
                )

                exported_users += 1

            if show_progress:
                print(f"[I] Exporting {exported_users} users", flush=True)

            if type(sleep_time) is int:
                sleep(sleep_time)
            elif sleep_time == "random":
                sleep_time = random.randint(1, 3)
            else:
                raise ValueError("Invalid sleep_time value")

        return []

    def __recover_users_and_enrolled(self, show_progress: bool = False) -> Tuple[List[User], Set[int]]:
        """
        Recover all users and enrolled users from the platform.

        This method is used to find users who have not yet completed the course.
        """
        # Steps: 1 - Get all users
        # Steps: 2 - Get users enrolled in courses
        # Steps: 3 - Find users who have not completed the course

        # Get all users
        all_users = list(self.get_users(only_students=True, enrollment_status=UserEnrollmentStatus.ALL, show_progress=show_progress))

        # Get all available courses
        users_with_course = set()
        for c, _ in Courses(self.auth).list_courses():
            users_with_course.update([
                x.identifier
                for x in self.get_users(only_students=True, enrolled_in_course=c.identifier, show_progress=show_progress)
            ])

        return all_users, users_with_course

    def get_leads(self, show_progress: bool = False) -> Iterable[User]:
        """
        Get all leads from the platform.

        A lead is a user who has not yet enrolled in any course.
        """
        # Steps: 1 - Get all users
        # Steps: 2 - Get users enrolled in courses
        # Steps: 3 - Find leads

        all_users, users_with_course = self.__recover_users_and_enrolled(show_progress=show_progress)

        # Find leads
        for user in all_users:
            if user.identifier not in users_with_course:
                yield user

    def get_contacts(self, show_progress: bool = False) -> Iterable[User]:
        """
        Get all contacts from the platform. Contact is a converted lead.
        """
        all_users, users_with_course = self.__recover_users_and_enrolled(show_progress=show_progress)

        # Find contacts
        for user in all_users:
            if user.identifier in users_with_course:
                yield user


__all__ = ("User", "Users", "UserType", "UserEnrollmentStatus")
