"""
    TrackingTime CSV export parser for Jira

    Assumes input file is comma delimited

    projects_time<dict>
        Proj1:  Task1: <time>
                Task2: <time>

        Proj2:  Task1: <time>

        Proj3:  Task1: <time>
                Task2: <time>
                Task3: <time>
"""

import csv
import json
from pprint import pprint


def convert_to_minutes(time_str):
    h, m = time_str.split(':')
    return int(h) * 60 + int(m)


def open_config(filename):
    with open(filename) as config:
        return json.load(config)


def main():
    config = open_config("config.json")
    csv_file = config["input"]["filename"]

    projects_time = dict()

    with open(csv_file, 'rb') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # If project exists
            if row["Project"] in projects_time:
                # If Task exists
                if row["Task"] in projects_time[row["Project"]]:
                    projects_time[row["Project"]][row["Task"]] += convert_to_minutes(row["Duration"])
                # Add new task to project
                else:
                    projects_time[row["Project"]][row["Task"]] = convert_to_minutes(row["Duration"])
            # Add new project to dictionary
            else:
                projects_time[row["Project"]] = {row["Task"]: convert_to_minutes(row["Duration"])}

    pprint(projects_time, width=1)

if __name__ == "__main__":
    main()
