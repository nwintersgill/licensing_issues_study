
import json, sqlite3, os
from itertools import combinations

#DATA_BASE = "reconcile.db"
INPUT_FILE = "response_codes.json"
# CODERS = 3

insert_questions = "INSERT INTO questions (qid, text) VALUES (?,?)"

insert_responses = "INSERT INTO responses (pid, qid, response) VALUES (?,?,?)"

insert_terms = "INSERT INTO terms (term, definition, qid) VALUES (?,?,?)"

def createResponseCodeInsertStatement(coders):
    statement = "INSERT INTO response_codes (qid, pid, "
    combos = all_combinations([f"R{i}" for i in range(coders)])
    statement += ", ".join(combos)
    fields = 2 + len(combos)
    statement += ") VALUES (" + (",".join(["?"]*fields)) + ")"
    return statement
        
def getDataFromFile(filename):
    if filename in ("response_codes.json", "glossary.json"):
        filename = os.path.join("generated_files", filename)
    else:
        filename = os.path.join("survey_files", filename)
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)
    
def all_combinations(input_list):
    all_combinations_list = []
    for r in range(1, len(input_list) + 1):
        all_combinations_list.extend(combinations(input_list, r))
    return ["".join(combo) for combo in all_combinations_list]
    
def getResponseCodeData(q, pid, d, coders):
    data = [q, int(pid)]
    codes = d[q][pid]
    for label in all_combinations([f"R{i}" for i in range(coders)]):
        data.append(" ".join(codes[label]))
    return data

def insertIntoDB(data, conn, query):
    cursor = conn.cursor()
    cursor.execute(query, data)

def addResponseCodesToDB(conn, coders, insert_response_codes):
    d = getDataFromFile(INPUT_FILE)
    for question in d:
        for response_id in d[question]:
            data = getResponseCodeData(question, response_id, d, coders)
            insertIntoDB(data, conn, insert_response_codes)
    conn.commit()

def addQuestionsToDB(conn):
    d = getDataFromFile("questions.json")
    for q, text in d.items():
        data = (q, text)
        insertIntoDB(data, conn, insert_questions)
    conn.commit()

def getResponseData(d):
    responses = []
    for pid in d:
        responses.append((int(pid), "D3", d[pid]["demographics"]["D3"]))
        for q in ["C1","C2","C3","C4","C6","C7"]:
            responses.append((int(pid), q, d[pid]["current_practice"][q]))
        for q in ["E2","E4","E6"]:
            responses.append((int(pid), q, d[pid]["experience"][q]))
        for q in ["EC1","EC3","EC5"]:
            responses.append((int(pid), q, d[pid]["edge_cases"][q]))
        for q in ["N2","N3","N4","N6" ]:
            responses.append((int(pid), q, d[pid]["needs"][q]))
    return responses
        
def addResponsesToDB(conn):
    d = getDataFromFile("responses.json")
    for response in getResponseData(d):
        insertIntoDB(response, conn, insert_responses)
    conn.commit()

def addTermsToDB(conn):
    d = getDataFromFile("glossary.json")
    for qid in d:
        for term in d[qid]:
            data = (term, d[qid][term], qid)
            insertIntoDB(data, conn, insert_terms)
    conn.commit()

def main(coders, db):
    insert_response_codes = createResponseCodeInsertStatement(coders)
    conn = sqlite3.connect(db)
    addResponseCodesToDB(conn, coders, insert_response_codes)
    addQuestionsToDB(conn)
    addResponsesToDB(conn)
    addTermsToDB(conn)
    conn.close()

if __name__ == "__main__":
    main()
