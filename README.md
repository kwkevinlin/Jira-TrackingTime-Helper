# TrackingTime Helper Script for Jira

A python helper script for [TrackingTime](https://chrome.google.com/webstore/detail/trackingtime-time-tracker/knailkjkjcfegledhjhcfacdngnicimb?hl=en-US) that aggregates total minutes spent for each task for easy entry into Jira.

### Input
A comma-delimited timesheet file exported from TrackingTime.

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
Timesheet files are automatically fetched from the downloads folder and moved to the local repo directory. Downloads and repo paths are defined in `config.json`. The export filename is also defined in config. The config should look like this:  
```JSON
{
    "input": {
        "src": "/downloads/folder",
        "dest": "/path/to/Jira/repo/folder"
    },
    "output": {
        "filename": "TimeBreakdown.csv",
        "keep_date": true
    }
}
```
`keep_date` determines if the output filename should have the date appended.

### Next Steps
Future release will include feature to automatically archive previously generated time-breakdown files into the archive foler.
