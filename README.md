# TrackingTime Helper Script for Jira

A python helper script for [TrackingTime](https://chrome.google.com/webstore/detail/trackingtime-time-tracker/knailkjkjcfegledhjhcfacdngnicimb?hl=en-US) that aggregates total minutes spent for each task for easy entry into Jira.

### Input
A comma-delimited file exported from TrackingTime for any given time period (usually two weeks for a sprint).

### Output
A comma-delimited file of the following format:  
  
| Project   | Task   | Time Spent (Minutes) |
|-----------|--------|----------------------|
| Project 1 | Task 1 | 320                  |
|           | Task 2 | 64                   |
| Project 2 | Task 1 | 123                  |
| Project 3 | Task 1 | 42                   |
|           | Task 2 | 214                  |
|           | Task 3 | 78                   |  

### Config
Input and outfile filenames are defined in the config, located in `config.json`. The config should look like this:  
```JSON
{
    "input": {
        "filename": "TrackingTime.csv"
    },
    "output": {
        "filename": "TimeBreakdown.csv"
    }
}
```
Both `filename` options are user-defined.

### Next Steps
Future releases will include automatic appending of sprint names to the end of the output file, as well as archiving of previously generated time-breakdown files to the archive folder.
