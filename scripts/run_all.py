
"""
Before converting JSON to CSV, make sure that the data directory has been created.
Before making any plots, make sure that the figs directory has been created.
TODO: Automate the creation of these folders if they do not already exist.
"""

from survey.csv2json import convertCSV
from partition import partition
from sanitize import sanitize
from json_converter import convert
from plot import plot

FROM_SOURCE = False # Code to run if building from original csv files (not included with remote)
PRE_PROCESS = False # pre-process the data before plotting
PLOT = True # plot figures for all surveys

all_surveys = ("survey",)

if PRE_PROCESS:
    if FROM_SOURCE:

        # Generate JSON Files from CSV
        convertCSV()

        # Sanitize JSON
        print("Sanitizing files...")
        for survey in all_surveys:
            sanitize(survey)

    ## Convert JSON to CSV
    print("Converting JSON to CSV...")
    for survey in all_surveys:
        convert(survey)

    ## Partition response coding
    print("Partitioning Response Coding Files...")
    for survey in ("survey",):
        partition(survey)

if PLOT:
    ## Plot the results
    print("Plotting Results (this may take awhile)...")
    for survey in all_surveys:
        print(f"Plotting {survey} survey...")
        plot(survey)

print("All Data Processed!")