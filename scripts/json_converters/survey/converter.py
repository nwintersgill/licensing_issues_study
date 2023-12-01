
from .. import AbstractConverter
from .config import *
import os

class Converter(AbstractConverter):

    def __init__(self, parent, file_name=""):
        AbstractConverter.__init__(self, file_name, parent)
        self.setConfigs()

    def setConfigs(self):
        self._ids = ids
        self._ranked = ranked
        self._multi = multi

    def rankedAnswer(self, question, data, role):

        participants = []
        formats = set()
        for p in data.values():

            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]   
              
            answer = eval("p" + types[question[:-1]])[question]

            for i, a in answer.items():
                if i != "other" and a != "":
                    full_answer = ranked_answers[question.lower()][int(i)-1]
                    
                    d[full_answer] = a
                    formats.add(full_answer)

            participants.append(d)

        path = os.path.join(role, "rank", question + ".csv")
        self.writeToFile(participants, path, shared+list(formats))

    def getMultiAnswer(self, question, data, role):

        participants = []
        formats = set()
        
        for p in data.values():

            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            qtype = question[:-1]
            answer = eval("p" + types[qtype])[question]
            keyword = "answers"

            if answer[keyword] == [""]:
                d["No Answer"] = 1
                formats.add("No Answer")
            else:
                for a in answer[keyword]:
                    d[a] = 1
                    formats.add(a)
                if answer["other"] != "":
                    d[answer["other"]] = 1
                    formats.add(answer["other"])

            participants.append(d)

        path = os.path.join(role, "multi_select", f"{question}.csv")
        self.writeToFile(participants, path, shared+list(formats))


    def getAllSingleAnswers(self, data, role):

        participants = []
        
        for p in data.values():
 
            d = {}
            d["ResponseID"] = p["meta"]["ResponseID"]

            d1 = p["demographics"]["D1"]
            d["D1"] = d1["other"] if d1["other"] != "" else d1["answers"]
            d["D2"] = p["demographics"]["D2"]

            d["C5"] = p["current_practice"]["C5"]

            d["E1"] = p["experience"]["E1"]
            d["E3"] = p["experience"]["E3"]
            d["E5"] = p["experience"]["E5"]

            d["EC2"] = p["edge_cases"]["EC2"]
            d["EC4"] = p["edge_cases"]["EC4"]

            n5 = p["needs"]["N5"]
            d["N5"] = n5["other"] if n5["other"] != "" else n5["answers"]

            participants.append(d)

        path = os.path.join(role, "single.csv")
        self.writeToFile(participants, path, shared+single)