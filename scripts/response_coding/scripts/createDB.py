
import sqlite3
from itertools import combinations

questions = '''
    CREATE TABLE "questions" (
	"id"	INTEGER NOT NULL UNIQUE,
	"qid"	TEXT NOT NULL,
	"text"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT))
    '''

response_codes = '''CREATE TABLE "response_codes" (
	"id"	INTEGER NOT NULL UNIQUE,
	"qid"	TEXT NOT NULL,
	"pid"	INTEGER NOT NULL,
	%s
	PRIMARY KEY("id" AUTOINCREMENT)
)'''

responses = '''CREATE TABLE "responses" (
	"id"	INTEGER NOT NULL UNIQUE,
	"pid"	INTEGER NOT NULL,
	"qid"	TEXT NOT NULL,
	"response"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)'''

terms = '''CREATE TABLE "terms" (
	"id"	INTEGER NOT NULL UNIQUE,
	"term"	TEXT NOT NULL,
	"definition"	TEXT NOT NULL,
	"qid"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)'''



## Duplicated from to_json.py (refactor opportunity)
def all_combinations(input_list):
    all_combinations_list = []
    for r in range(1, len(input_list) + 1):
        all_combinations_list.extend(combinations(input_list, r))
    return ["".join(combo) for combo in all_combinations_list]

def createResponseCodeTableStatement(coder_num):
    labels = all_combinations([f"R{i}" for i in range(coder_num)])
    statement = ""
    for label in labels:
        statement += f'\"{label}\" TEXT,\n'
    return response_codes % (statement,)


def main(coders, db_name):

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    statements = [questions, responses, terms, createResponseCodeTableStatement(coders)] 

    for statement in statements:

        cursor.execute(statement)
        conn.commit()

    conn.close()

    print("Database and schema created successfully.")
