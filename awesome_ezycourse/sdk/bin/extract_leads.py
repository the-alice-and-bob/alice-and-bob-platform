import os
import csv
import pickle
import argparse
from dataclasses import dataclass

from typing import List
from datetime import datetime

from awesome_ezycourse.sdk import User


@dataclass
class CSVCourse:
    course: str
    student_name: str
    user_email: str
    start_date: datetime
    complete_date: datetime
    last_visit_in: datetime
    progress_report: int
    course_id: int

    user_id: int = None


# Function to transform CSV data into User dataclass
def load_csv_course(course_id: int, csv_path: str) -> List[CSVCourse]:
    """
    CSV Format:

    "course","student_name","email","start_date","complete_date","last_visit_in","progress_report"
    "102 - API Security Checklist","xxxx","xxx@xxx.com","NA","NA","NA","0"

    """
    with open(csv_path, "r", encoding='utf-8-sig') as csv_file:
        # REad csv line by line
        reader = csv.DictReader(csv_file)

        entries = []

        for row in reader:
            entries.append(CSVCourse(
                course=row["course"],
                student_name=row["student_name"],
                user_email=row["email"],
                start_date=datetime.strptime(row["start_date"], "%Y-%m-%d"),
                complete_date=datetime.strptime(row["complete_date"], "%Y-%m-%d"),
                last_visit_in=datetime.strptime(row["last_visit_in"], "%Y-%m-%d"),
                progress_report=int(row["progress_report"]),
                course_id=course_id
            ))

    return entries


def find_leads(users, course_info) -> List[User]:
    leads = []
    for user in users:
        for course in course_info:
            if user.email == course.user_email:
                course.user_id = user.id
                break


def main(parsed):
    current_path = os.getcwd()

    with open(os.path.join(current_path, parsed.users_pickle), "rb") as f:
        users = pickle.load(f)

    courses = []

    for c in parsed.course_csv:
        courses.append(load_csv_course(c, os.path.join(current_path, c)))

    leads = find_leads(users, courses)

    print(leads)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load students from pickle and complete the course missing data")
    parser.add_argument("-u", "--users-pickle", help="Pickle file with students data")
    parser.add_argument("-o", "--output-csv", help="Output CSV file with completed course data")
    parser.add_argument("course_csv", nargs="+", help="CSV files with complete course data")
    args = parser.parse_args()

    main(args)
