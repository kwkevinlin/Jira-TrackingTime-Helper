"""
    TrackingTime CSV export parser for Jira

    Assumes input file is comma delimited
"""

import csv

filename = "TrackingTime.csv"

projects_time = dict()

with open(filename, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print "Project: {},\tTask: {},\tTime: {}".format(row["Project"], row["Task"], row["Duration"])

        # If project exists
        if row["Project"] in projects_time:
            # If Task exists
            if row["Task"] in projects_time["Projects"]:
                projects_time["Projects"]["Task"] += row["Duration"]
            # Add new task to project
            else:
                projects_time["Projects"]["Task"] = row["Duration"]
        # Add new project to dictionary
        else:
            projects_time[row["Project"]] = {row["Task"]: row["Duration"]}

"""
End result:
Proj1:  Task1: <time>
        Task2: <time>

Proj2:  Task1: <time>

Proj3:  Task1: <time>
        Task2: <time>
        Task3: <time>
"""
