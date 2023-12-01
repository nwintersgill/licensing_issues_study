
import csv, os, json, shutil, glob
from json_converters.survey import ids

def main():
    survey  = "survey"
    partition(survey)

def partition(survey):
    Partition(survey).run()
    
class Partition():

    def __init__(self, survey):

        assert survey in ("survey",)

        self._survey = survey
        self._ids = ids
        self._valid = self.getValid()

    def getValid(self):
        path = os.path.join("survey", "files", "valid.txt")
        if os.path.isfile(path):
            with open(path, "r") as file:
                return [pid.strip() for pid in file.readlines()]
        else:
            return list(self.getJsonData().keys())

    def run(self):
        codes = self.getCodingData()
        data = self.getJsonData()
        self.saveAll()
        self.saveLoose(codes, data)
        self.saveStrict(codes, data)

    def getDataPath(self):
        return os.path.join(self._survey, "data")

    def getFilePath(self):
        return os.path.join(self._survey, "files")

    def getMostRecent(self):
        path = os.path.join(self.getFilePath(), "*sanitized_*.json")
        return glob.glob(path)[-1]

    def getCodingData(self):
        path = os.path.join(self.getDataPath(), "response_coding.csv")
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            return [row for row in reader]
        
    def getJsonData(self):
        path = self.getMostRecent()
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
        
    def saveAll(self):
        shutil.copy(os.path.join(self.getDataPath(), "response_coding.csv"),
                    os.path.join(self.getDataPath(), "all", "response_coding.csv"))
        
    def getRole(self, data, pid):
        if pid in self._valid:
            return data[pid]["demographics"]["D1"]["answers"]
        else:
            return None

    def saveLoose(self, codes, data):
        for r in self._ids.keys():
            path = os.path.join(self.getDataPath(), "loose", r, "response_coding.csv")
            with open(path, "w", encoding="utf-8") as file:
                writer = csv.writer(file, lineterminator='\n')
                for i, row in enumerate(codes):
                    if i == 0:
                        writer.writerow(row)
                    else:
                        pid = row[0]
                        role = self.getRole(data, pid)
                        if role != None and self._ids[r] in role:
                            writer.writerow(row)

    def saveStrict(self, codes, data):
        path = os.path.join(self.getDataPath(), "strict")
        if os.path.isdir(path):
            roles = os.listdir(path)
            for r in roles:
                path = os.path.join(self.getDataPath(), "strict", r, "response_coding.csv")
                with open(path, "w", encoding="utf-8") as file:
                    writer = csv.writer(file, lineterminator='\n')
                    for i, row in enumerate(codes):
                        if i == 0:
                            writer.writerow(row)
                        else:
                            pid = row[0]
                            target = set([self._ids[role] for role in r.split("-")])
                            role = self.getRole(data, pid)
                            if role != None and target == role:
                                writer.writerow(row)

if __name__ == "__main__":
    main()
