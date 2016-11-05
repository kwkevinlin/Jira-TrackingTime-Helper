"""
    TrackingTime CSV export parser for Jira

    Assumes input file is comma delimited
"""

import csv
from pprint import pprint


def convert_to_minutes(time_str):
    h, m = time_str.split(':')
    return int(h) * 60 + int(m)


filename = "TrackingTime.csv"

projects_time = dict()

with open(filename, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
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

        


"""
End result:
Proj1:  Task1: <time>
        Task2: <time>

Proj2:  Task1: <time>

Proj3:  Task1: <time>
        Task2: <time>
        Task3: <time>
"""
