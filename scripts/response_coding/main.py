
"""
- Complete steps 1-3 to set up The Grand Reconciliator (move database to reconciliator/reconciliator)
- Reconcile the codes
- Then run step 4
"""
from scripts import comparer, to_json, pull_comments, createDB, populateDB, reconcile

CODERS = 3
DB_NAME = "reconcile.db"

## Step 1: Compare codes across annotators
### Download response codes and place them in code_files folder
if False:
    comparer.main(CODERS)
    to_json.main(CODERS)

## Step 2: Create glossary from code book
### Download the code book and save it to code_files/dictionary.xlsx
if False:
    pull_comments.main()

## Step 3: Create and populate the database
### Make sure that questions.json and responses.json are in the survey_files folder
if True:
    createDB.main(CODERS, DB_NAME)
    populateDB.main(CODERS, DB_NAME)

## Step 4: Merge reconciliation with agreed codes
### Download reconciliation and place in the code_files folder
### You may need to manually add back the response IDs
if False:
    reconcile.main()