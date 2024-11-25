"""
This file reads a CSV with purchase orders and sends them to a webhook as JSON data to Zoho Webhook

CSV Format:

course,course id,student id,student_name,email,start_date,complete_date,last_visit_in,progress_report
102 - API Security Checklist,13232,710217,xxxxx,xx@xxx.com,,,,0
"""

import csv
import json
import argparse

import requests


def main(args):
    with open(args.csv_file, "r", encoding='utf-8-') as f:
        reader = csv.DictReader(f)

        """
        CSV Format:
        course,course_id,student_id,student_name,email,start_date,complete_date,last_visit_in,progress_report

        """

        # Skip the header
        for row in reader:
            try:
                data = {
                    "course": row["course"],
                    "course_id": int(row["course_id"]),
                    "student_id": int(row["student_id"]),
                    "student_name": row["student_name"],
                    "email": row["email"],
                    "start_date": row["start_date"],
                    "complete_date": row["complete_date"],
                    "last_visit_in": row["last_visit_in"],
                    "progress_report": int(row["progress_report"])
                }
            except ValueError as e:
                print(f"Error parsing row: {row}")
                continue

            if args.dry_run:
                print(json.dumps(data, indent=2))
            else:
                print(f"Importing purchase order for '{data['student_name']}' and course '{data['course']}'")

                response = requests.post(args.webhook, json=data)
                response.raise_for_status()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Import purchase orders rom CSV file and send to webhook converted to JSON")
    parser.add_argument("csv_file", help="CSV file with purchase orders")
    parser.add_argument("webhook", help="Webhook URL")
    parser.add_argument("--dry-run", action="store_true", help="Do not send the data to the webhook")
    args = parser.parse_args()

    main(args)
