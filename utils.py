"""
    Utility functions for main driver
"""

import csv
import json
from utils import *
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


def is_new_project(row, projects_time):
    return not row["Project"] in projects_time


def is_new_task(row, projects_time):
    return not row["Task"] in projects_time[row["Project"]]


def is_new_date(row, projects_time, task_date):
    return task_date not in projects_time[row["Project"]][row["Task"]]


def create_new_project(row, projects_time):
    projects_time[row["Project"]] = {}


def create_new_task(row, projects_time):
    projects_time[row["Project"]][row["Task"]] = {}


def create_new_task_time_at_date(row, projects_time, task_date):
    projects_time[row["Project"]][row["Task"]][task_date] = convert_to_minutes(row["Duration"])


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

    with open(filename, 'wb') as file:
        writer = csv.writer(file)
        writer.writerow(["Project", "Task", "Date", "Time Spent (Minutes)"])

        for project, tasks in projects_time.items():
            first_index = project
            for task, days in tasks.items():
                second_index = task
                for day, time_spent in days.items():
                    writer.writerow([first_index, second_index, day, time_spent])
                    first_index = ""
                    second_index = ""
