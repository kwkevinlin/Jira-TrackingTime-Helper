"""
    TrackingTime CSV export parser for Jira

    Assumes input file is comma delimited

    Work log grouped in order of:
        Project -> Task -> Day -> Aggregated time for that day (in minutes)

"""

from utils import *
from pprint import pprint

"""
    TODO:
        Dates are not outputting in order, but pprint is
        Total hours worked
        Option in config by day or week
        Sprint naming for CSV
"""


def main():
    config = open_config("config.json")
    input_csv = config["input"]["filename"]

    projects_time = read_data_to_dict(input_csv)

    pprint(projects_time, indent=4, width=1)

    write_processed_data_to_csv(projects_time, config)


if __name__ == "__main__":
    main()
