import json, os, glob, re

from json_converters.survey import config


surveys = ("survey",)

regex = re.compile("([A-Z]{1,2}\d+) (\d+)", re.IGNORECASE)

def getConfig(survey):
    if survey == "survey": return config
    else: return {}

def getValidQuestions(survey):
    survey = survey.replace(" ", "_")
    path = os.path.join(survey, "questions.json")
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
        
def getMostRecent(survey):
    path = os.path.join(survey, "files", "*sanitized_*.json")
    if len(glob.glob(path)) == 0:
        print("Unable to find response data for survey '" + survey + "', exiting.")
        exit(1)
    return glob.glob(path)[-1].split(os.sep)[-1]

def getData(survey):
    survey = survey.replace(" ", "_")
    if survey == "initial": survey = "initial_survey"
    path = os.path.join(survey, "files", getMostRecent(survey))
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def getValidUserIDs(data):
    return sorted([int(k) for k in data.keys()])
    
def getQuestion(survey, valid):
    while True:
        qid = input(">>> Enter a question ID: ").upper().strip()
        if qid in valid:
            print(f"Question {qid} selected.")
            return qid
        else:
            print(f"{qid} is not a valid question ID for the {survey} survey.")

def getUserID(survey, valid):
    while True:
        pid = int(input(">>> Enter a participant ID: ").strip())
        if pid in valid:
            print(f"Participant {pid} selected.")
            return pid
        else:
            print(f"{pid} is not a valid participant ID for the {survey} survey.")

def getResponse(data, survey, question, user):
    config = getConfig(survey)
    qtype = re.search("([A-Z]{1,2})\d+", question).group(1)
    if survey in ("initial", "machine learning", "legal"):
        return data[str(user)][config.types[qtype]][question]
    else:
        p = data[str(user)]
        return eval("p" + config.types[qtype])[question]
    
def getNextValidIndex(valid_pids, user):
    new = valid_pids.index(user) + 1
    if new >= len(valid_pids): return -1
    else: return new

def selectSurvey():
    survey = "survey"
    data = getData(survey)
    question, user, valid_pids, valid_questions = selectQuestion(survey, data)
    return data, survey, question, user, valid_pids, valid_questions

def selectQuestion(survey, data):
    valid_questions = getValidQuestions(survey)
    question = getQuestion(survey, valid_questions.keys())
    user, valid_pids = selectUser(survey, data)
    return question, user, valid_pids, valid_questions

def selectUser(survey, data):
    valid_pids = getValidUserIDs(data)
    user = getUserID(survey, valid_pids)
    return user, valid_pids

def printResponse(data, survey, question, user, valid_pids, valid_questions):
    resp = getResponse(data, survey, question, user)
    if resp == "": resp = "<No Response>"
    fields = (question, valid_questions[question], str(user), resp)
    print("\nQuestion: %s - %s\nParticipant: %s\nResponse:\n\n%s\n" % fields)
    return getNextValidIndex(valid_pids, user)

def main():

    print()
    print("Welcome to the Data Viewer!")
    print("Type a question ID and a participant ID to begin.")
    print("After your first response has been displayed, type 'help' for more information.")
    print()

    data, survey, question, user, valid_pids, valid_questions = selectSurvey()

    printResponse(data, survey, question, user, valid_pids, valid_questions)

    index = getNextValidIndex(valid_pids, user)
    while True:
        user = valid_pids[index]
        selection = input(">>> ")
        
        if selection == "":
            if index < 0:
                print("There are no more valid responses.")
            else:
                index = printResponse(data, survey, question, user, valid_pids, valid_questions)

        elif re.fullmatch("([A-Za-z]{1,2})\d+", selection):
            if selection.upper() in valid_questions.keys():
                question = selection.upper()
                user, valid_pids = selectUser(survey, data)
                index = printResponse(data, survey, question, user, valid_pids, valid_questions)
            else:
                print("Unknown question ID.")

        elif selection.isdigit():
            if int(selection) in valid_pids:
                user = int(selection)
                index = printResponse(data, survey, question, user, valid_pids, valid_questions)
            else:
                print("Unknown participant ID.")

        elif regex.match(selection):

            m = regex.match(selection)

            q = m.group(1).upper()
            if q in valid_questions.keys(): 
                u = int(m.group(2))
                if u in valid_pids: 
                    question = q
                    user = u
                    index = printResponse(data, survey, question, user, valid_pids, valid_questions)
                else:
                    print("Invalid participant ID")
            else:
                print("Invalid question ID.")


        elif selection.lower() == "exit" or selection.lower() == "quit":
            print("Good-bye.")
            break

        elif selection.lower() == "help":
            print()
            print("Type a question ID or participant ID to navigate.")
            print("Type both like '<question id> <participant id>' for fast navigation.")
            print("Hit enter to see the next valid response.")
            print("Type 'questions' to see available question IDs.")
            print("Type 'responses' to see available response IDs.")
            print("Type 'current' to see current selections.")
            print("Type 'show <question id>' to see that question's text.")
            print("Type 'exit' or 'quit' to quit.")
            print("Type 'help' to see this page.")
            print()

        elif selection.lower() == "current":
            print()
            print("Question:", question)
            print("Participant:", user)
            print()

        elif re.match("show (([A-Za-z]{1,2})\d+)", selection, re.IGNORECASE):
            q = re.match("show ([A-Za-z]{1,2}\d+)", selection, re.IGNORECASE).group(1)
            print(f"\n{valid_questions[q.upper()]}\n")

        elif selection.lower() == "questions":
            print(sorted(list(valid_questions.keys())))

        elif selection.lower() == "responses":
            print(valid_pids)

        else:
            print("Unknown command.")
        
main()