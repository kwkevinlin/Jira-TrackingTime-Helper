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


def is_not_new_project(row, projects_time):
    return row["Project"] in projects_time


def is_new_task(row, projects_time):
    return row["Task"] in projects_time[row["Project"]]


def add_time_to_task(row, projects_time):
    projects_time[row["Project"]][row["Task"]] += convert_to_minutes(row["Duration"])


def set_time_for_task(row, projects_time):
    projects_time[row["Project"]][row["Task"]] = convert_to_minutes(row["Duration"])


def create_new_project(row, projects_time):
    projects_time[row["Project"]] = {row["Task"]: convert_to_minutes(row["Duration"])}


def write_output_to_file(projects_time, config):
    filename = config["output"]["filename"]

    if (config["output"]["format"] == "csv"):
        with open(filename + ".csv", 'wb') as file:
            writer = csv.writer(file)
            writer.writerow(["Project", "Task", "Time Spent (Minutes)"])

            for project, tasks in projects_time.items():
                print("Project: " + project)
                tasks_row = []

                first_index = project
                for task in tasks:
                    tasks_row.append([first_index, task, tasks[task]])
                    first_index = ""

                for row in tasks_row:
                    writer.writerow(row)

                print(tasks_row)


def main():
    config = open_config("config.json")
    csv_file = config["input"]["filename"]

    projects_time = dict()

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if is_not_new_project(row, projects_time):  # Change order of this
                if is_new_task(row, projects_time):
                    add_time_to_task(row, projects_time)
                else:
                    set_time_for_task(row, projects_time)
            else:
                create_new_project(row, projects_time)

    write_output_to_file(projects_time, config)

if __name__ == "__main__":
    main()
