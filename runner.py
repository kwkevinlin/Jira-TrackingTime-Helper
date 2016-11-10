"""
    TrackingTime CSV export parser for Jira

    Assumes input file is comma delimited

    Work log grouped in order of:
        Project -> Task -> Day -> Aggregated time for that day (in minutes)

    projects_time<dict>
        Proj1:  Task1: Day1: 102
                       Day2: 43
                Task2: Day6: 75

        Proj2:  Task1: Day4: 52

        Proj3:  Task1: Day2: 12
                Task2: Day1: 167
                       Day8: 128
                Task3: Day5: 52
                       Day6: 71
                       Day9: 68
"""

import csv
import json
from pprint import pprint
from datetime import datetime


def open_config(filename):
    with open(filename) as config:
        return json.load(config)


def get_formatted_task_date(date):
    task_date = datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
    return "{}/{}".format(task_date.month, task_date.day)


def convert_to_minutes(time_str):
    h, m = time_str.split(':')
    return int(h) * 60 + int(m)


# =======


def is_new_project(row, projects_time):
    return not row["Project"] in projects_time


def is_new_task(row, projects_time):
    return not row["Task"] in projects_time[row["Project"]]


def is_new_date(row, projects_time, task_date):
    # This is always returning true because dict is always empty
    # Why is dict task's time entry empty?
    return task_date not in projects_time[row["Project"]][row["Task"]]

# =======


def create_new_project(row, projects_time):
    projects_time[row["Project"]] = {}


def create_new_task(row, projects_time):
    projects_time[row["Project"]][row["Task"]] = {}

# =======


def create_new_task_time_at_date(row, projects_time, task_date):
    # print("Before")
    # pprint(projects_time[row["Project"]][row["Task"]])
    projects_time[row["Project"]][row["Task"]][task_date] = convert_to_minutes(row["Duration"])
    # print("After")
    # pprint(projects_time[row["Project"]][row["Task"]])


def add_task_time_to_existing_date(row, projects_time, task_date):
    projects_time[row["Project"]][row["Task"]][task_date] += convert_to_minutes(row["Duration"])


def add_time_to_task(row, projects_time, task_date):
    if is_new_task(row, projects_time):
        create_new_task(row, projects_time)
        if is_new_date(row, projects_time, task_date):
            create_new_task_time_at_date(row, projects_time, task_date)
        else:
            add_task_time_to_existing_date(row, projects_time, task_date)
    else:
        if is_new_date(row, projects_time, task_date):
            create_new_task_time_at_date(row, projects_time, task_date)
        else:
            add_task_time_to_existing_date(row, projects_time, task_date)


def read_data_to_dict(input_csv):
    projects_time = {}
    with open(input_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            task_date = get_formatted_task_date(row["Start Date"])
            if is_new_project(row, projects_time):
                create_new_project(row, projects_time)
                add_time_to_task(row, projects_time, task_date)
            else:
                add_time_to_task(row, projects_time, task_date)

    return projects_time


def write_processed_data_to_csv(projects_time, config):
    filename = config["output"]["filename"]

    # Get time then add to filename for backup
    # Delete after 2 sprints (only keep 2 in folder)

    with open(filename, 'wb') as file:
        writer = csv.writer(file)
        writer.writerow(["Project", "Task", "Time Spent (Minutes)"])

        for project, tasks in projects_time.items():
            first_index = project
            for task in tasks:
                writer.writerow([first_index, task, tasks[task]])
                first_index = ""

"""
    TODO:
        Confirm if output is correct
        Option in config by day or week

    Potential Issue:
        Use OrderedDict to keep dates in order. Or else 1/1 might show up before 12/31.
"""


def main():
    config = open_config("config.json")
    input_csv = config["input"]["filename"]

    projects_time = read_data_to_dict(input_csv)

    pprint(projects_time, indent=4, width=1)

    # write_processed_data_to_csv(projects_time, config)


if __name__ == "__main__":
    main()
