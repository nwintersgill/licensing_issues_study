# "The Law Doesn’t Work Like a Computer": Exploring Software Licensing Issues Faced by Legal Practitioners

Link to preprint: https://arxiv.org/abs/2403.14927

## What is Included
- `scripts/`: Python scripts used for data cleaning, open-coding, reconciliation, and data analysis
- `figures/`: Aggregate plots of survey data (broken down at the role-level)
- `interview_protocol.pdf`: The protocol followed for follow-up interviews
- `glossary.json`: Glossary of codes and definitions (per question) resulting from open-coding
- `survey_questions.pdf`: A PDF of the full survey text (including questions), as seen by participants, produced by Qualtrics
- `questions.json`: A JSON of questions, in short form, and their associated IDs

## What is Not Included
In order to follow our approved research protocol and preserve our survey participants' anonymity, individual responses are not included in this replication package. The nature of the responses we received means that even redacted responses could reveal the identities of individual participants.

NOTE: This means that the scripts may not run out of the box.  They require data files in order to function properly.

## Installation

In order to run the data cleaning and analysis tools, the following libraries will need to be installed.

- `pip install pandas`
- `pip install matplotlib`
- `pip install django`

## Directory Structure

### Figures

The `figures` folder contains plots showing aggregated results from each question in our survey. The `all` subfolder includes plots showing all answers to a given question, and the `loose` folder contains plots showing the answers provided by specific self-identified subgroups of respondents: in-house legal counsel, coutside legal counsel, and those who specified another role in the 'other' field.


### Scripts 

The `scripts` folder contains the scripts that were used to process and analyze the survey data we collected. *Importantly, scripts that require full survey responses will not function, as full responses are omitted from this repository to preserve participants' anonymity. This includes the `data_reader.py` and `run_all.py` scripts.* However, the scripts are included here to allow others to verify the process behind our analysis and to provide a scaffold for future surveys. The `data_reader.py` utility allows easy viewing of survey data, when present. The `run_all.py` utility incorporates the other files in the directory to fully preprocess and plot the survey data. 

#### JSON Converters
The files in the `json_converters` subfolder are utilized by `run_all.py` to preprocess raw survey data into a readable format.

#### Response Coding

The `response_coding` subfolder contains scripts and tools that were used in our *open coding* of survey responses. Specifically, these tools were used to reconcile differences between the annotators' independent open coding results and reach a consensus on the codes that should apply to each response. `main.py` details how to set up the main tool, the reconciliator. The `reconciliator` subfolder contains the tool itself. Running `python reconciliator/reconciliator/manage.py runserver` will start a django application. While it is running, open a web broweser and connect to http://127.0.0.1:8000/ to view the reconciliator. *Note that this tool requires the survey data and the annotators' codes to run correctly.*