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


def is_new_project(row, projects_time):
    return not row["Project"] in projects_time


def create_new_project(row, projects_time):
    projects_time[row["Project"]] = {row["Task"]: convert_to_minutes(row["Duration"])}


def is_new_task(row, projects_time):
    return not row["Task"] in projects_time[row["Project"]]


def set_time_for_new_task(row, projects_time):
    projects_time[row["Project"]][row["Task"]] = convert_to_minutes(row["Duration"])


def add_time_to_existing_task(row, projects_time):
    projects_time[row["Project"]][row["Task"]] += convert_to_minutes(row["Duration"])


def read_data_to_dict(input_csv):
    projects_time = dict()
    with open(input_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if is_new_project(row, projects_time):
                create_new_project(row, projects_time)
            else:
                if is_new_task(row, projects_time):
                    set_time_for_new_task(row, projects_time)
                else:
                    add_time_to_existing_task(row, projects_time)

    return projects_time


def write_processed_data_to_csv(projects_time, config):
    filename = config["output"]["filename"]

    with open(filename, 'wb') as file:
        writer = csv.writer(file)
        writer.writerow(["Project", "Task", "Time Spent (Minutes)"])

        for project, tasks in projects_time.items():
            first_index = project
            for task in tasks:
                writer.writerow([first_index, task, tasks[task]])
                first_index = ""


def main():
    config = open_config("config.json")
    input_csv = config["input"]["filename"]

    projects_time = read_data_to_dict(input_csv)

    pprint(projects_time, indent=4, width=1)

    write_processed_data_to_csv(projects_time, config)


if __name__ == "__main__":
    main()
