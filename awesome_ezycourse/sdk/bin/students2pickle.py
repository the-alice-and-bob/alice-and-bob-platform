import os
import csv
import pickle
import argparse

from typing import Dict
from datetime import datetime

from awesome_ezycourse.sdk.users import User


# Function to transform CSV data into User dataclass
def csv_to_dataclass(csv_path: str) -> Dict[str, User]:
    """
    CSV Format:

    "id","name","email","status","created_at","last_login"
    "663050","Demo Demo","xx@xx.com","","2024-05-16T10:12:03.000+00:00","2024-10-18T06:04:34.000+00:00"

    """
    with open(csv_path, "r") as csv_file:
        # REad csv line by line
        reader = csv.reader(csv_file)

        entries = {}

        # Skip the header
        next(reader)

        for row in reader:

            try:
                created_at = datetime.fromisoformat(row[4])
            except ValueError:
                created_at = None

            try:
                last_login = datetime.fromisoformat(row[5])
            except ValueError:
                last_login = None

            entries[row[2]] = User(
                identifier=int(row[0]),
                full_name=row[1],
                email=row[2],
                status=row[3],
                created_at=created_at,
                last_login=last_login
            )

    return entries


def main(parsed):
    current_path = os.getcwd()

    users = csv_to_dataclass(os.path.join(current_path, parsed.csv_file))

    with open(os.path.join(current_path, args.pickle_file), "wb") as f:
        pickle.dump(users, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load students from csv and save them to a pickle file")
    parser.add_argument("csv_file", help="CSV file with students data")
    parser.add_argument("pickle_file", help="Pickle file to save students data")
    args = parser.parse_args()

    main(args)
