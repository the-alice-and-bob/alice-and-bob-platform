import os
import csv
import pickle
import argparse
from dataclasses import dataclass

from typing import List
from datetime import datetime

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
    "102 - API Security Checklist","XXX","xx@xxx.com","NA","NA","NA","0"

    """
    with open(csv_path, "r", encoding='utf-8-sig') as csv_file:
        # REad csv line by line
        reader = csv.reader(csv_file)

        entries = []

        # Skip the header
        next(reader)

        for row in reader:

            try:
                start_date = datetime.fromisoformat(row[3])
            except ValueError:
                start_date = None

            try:
                complete_date = datetime.fromisoformat(row[4])
            except ValueError:
                complete_date = None

            try:
                last_visit_in = datetime.fromisoformat(row[5])
            except ValueError:
                last_visit_in = None

            entries.append(CSVCourse(
                course=row[0],
                student_name=row[1],
                user_email=row[2],
                start_date=start_date,
                complete_date=complete_date,
                last_visit_in=last_visit_in,
                progress_report=int(row[6]),
                course_id=course_id
            ))

    return entries


def complete_course_data(users, course_info: List[CSVCourse]):
    for course in course_info:
        try:
            course.user_id = users[course.user_email].identifier
        except KeyError:
            print(f"User with email '{course.user_email}' not found")
            continue

    return users


def dump_csv_course(course_info: List[CSVCourse], csv_path):
    """
    CSV Format:
    "course", "course id", "student id","student_name","email","start_date","complete_date","last_visit_in","progress_report"
    """
    with open(csv_path, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, quoting=csv.QUOTE_ALL, fieldnames=[
            "course", "course_id", "student_id", "student_name", "email", "start_date", "complete_date", "last_visit_in",
            "progress_report"
        ])

        writer.writeheader()

        for course in course_info:
            writer.writerow({
                "course": course.course,
                "course_id": course.course_id,
                "student_id": course.user_id,
                "student_name": course.student_name.strip(),
                "email": course.user_email,
                "start_date": course.start_date,
                "complete_date": course.complete_date,
                "last_visit_in": course.last_visit_in,
                "progress_report": course.progress_report
            })


def main(parsed):
    current_path = os.getcwd()

    with open(os.path.join(current_path, parsed.users_pickle), "rb") as f:
        users = pickle.load(f)

    course_info = load_csv_course(parsed.course_id, os.path.join(current_path, parsed.course_csv))

    complete_course_data(users, course_info)

    dump_csv_course(course_info, os.path.join(current_path, parsed.output_csv))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load students from pickle and complete the course missing data")
    parser.add_argument("users_pickle", help="Pickle file with students data")
    parser.add_argument("course_csv", help="CSV file with course data")
    parser.add_argument("course_id", help="Course ID to complete")
    parser.add_argument("output_csv", help="Output CSV file with completed course data")
    args = parser.parse_args()

    main(args)
