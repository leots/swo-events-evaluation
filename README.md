# swo-events-evaluation
Code used for the evaluation of detected events in the Social Web Observatory platform.

## Requirements
The code requires Python 3.6 or later to run.

The annotators run the `evaluation.py` script, which reads events from the `events_out` folder and asks them to answer 3 questions per event. The answers are saved in a `lastSession.pickle` file.

To transform the answers into CSV format for further analysis you can use the `extractOutcomes.py` script.

## Data
**todo...**
In order to prevent uploading the content of articles here, we have removed the article texts from the JSON files. To perform the same experiment, you can use the URLs that are in the data and scrape the article content yourself in order to produce the "full" JSON files required for human annotation.
