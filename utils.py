"""
    Utility functions for main driver
"""

import os
import re
import sys
import csv
import json
from utils import *
from pprint import pprint
from datetime import datetime


def open_config(filename):
    with open(filename) as config:
        return json.load(config)


def move_timesheet_to_working_folder(config):
    for filename in os.listdir(config["input"]["src"]):
        if "TrackingTime" in filename:
            source = "{}/{}".format(config["input"]["src"], filename)
            destination = "{}/{}".format(config["input"]["dest"], filename)
            os.rename(source, destination)
            print("Moved '{}' to Jira folder\n".format(filename))


def read_input_timesheet(config):
    input_file_list = []
    for filename in os.listdir("."):
        if "TrackingTime" in filename:
            input_file_list.append(filename)

    if len(input_file_list) > 1:
        index = 1
        print("\nWarning!\nMultiple TrackingTime CSV files found:")
        for file in input_file_list:
            print("\t{}. {}".format(index, file))
            index += 1
        filename_index = raw_input("Enter the correct filename index: ")
        filename_index = validate_and_realign_index(filename_index, index - 1)
        filename = input_file_list[filename_index]
        print("\nUsing '{}'\n\n".format(filename))
        add_input_filename_to_config(config, filename)
        return filename
    elif len(input_file_list) == 0:
        sys.exit("\nError! No input file found with 'TrackingTime' in filename.\n" +
                 "Script terminated.\n")
    else:
        filename = input_file_list[0]
        add_input_filename_to_config(config, filename)
        return input_file_list[0]


def validate_and_realign_index(filename_index, index):
    if filename_index == "":
        sys.exit("\nInvalid index. Clean your glasses and try again!\n")
    filename_index = int(filename_index)
    if filename_index > index or filename_index < 0:
        sys.exit("\nInvalid index. Read carefully and try again!\n")
    return filename_index - 1


def add_input_filename_to_config(config, filename):
    config["input"] = {
        "filename": filename
    }


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
    projects_time[row["Project"]][row["Task"]][task_date] = convert_to_minutes(row["Duration"]) * 1.00


def add_task_time_to_existing_date(row, projects_time, task_date):
    projects_time[row["Project"]][row["Task"]][task_date] += convert_to_minutes(row["Duration"]) * 1.00


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


def write_processed_data_to_csv(config, projects_time):
    filename = get_output_filename(config)

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


def get_output_filename(config):
    input_filename = config["input"]["filename"]
    output_filename = config["output"]["filename"]

    if config["output"]["keep_date"]:
        date = ""
        try:
            date = get_report_end_date(input_filename)
            sub_name = output_filename.partition(".csv")
            output_filename = sub_name[0] + " - " + date + sub_name[1]
        except Exception as e:
            if input_filename == "TrackingTime.csv":
                print ("\nWarning!\nNo dates detected in input file '{}'. " +
                       "Using config filename '{}'.").format(input_filename, output_filename)
            else:
                print ("\nWarning!\nSomething went wrong in utils.py.get_output_filename. " +
                       "Using config filename '{}'.").format(output_filename)

    print("\nDone!\nProject time tracking breakdown written to '{}'\n".format(output_filename))
    return output_filename


def get_report_end_date(input_filename):
    return re.search("TrackingTime .* - (.*), \d{4}.csv", input_filename).group(1)
