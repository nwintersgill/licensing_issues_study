
import os, json, glob

def getFilePath(directory):
    return os.path.join(directory, "files")

def getLatest(directory):
    path = os.path.join(getFilePath(directory), "*completers_*.json")
    files = glob.glob(path)
    files = sorted([f.split(os.sep)[-1][:-5] for f in files])
    return files[-1] + ".json"

def getJSON(directory):
    path = os.path.join(getFilePath(directory), 
                        getLatest(directory))
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def getValid(d, directory):
    path = os.path.join(getFilePath(directory), "valid.txt")
    if os.path.isfile(path): 
        with open(path, "r") as file:
            return [pid.strip() for pid in file.readlines()]
    return d.keys()
    
def removeInvalid(d, directory):
    valid = getValid(d, directory)
    pids = list(d.keys())
    for pid in pids:
        if not pid in valid:
            d.pop(pid)

def removePII(d, directory):
    for resp in d.values():
        resp.pop("consent")
        resp["meta"].pop("IPAddress")
        resp.pop("contact_information")
        resp["meta"].pop("LocationLatitude")
        resp["meta"].pop("LocationLongitude")

def saveJSON(d, directory):
    path = os.path.join(getFilePath(directory), 
                        getLatest(directory).replace("completers","sanitized"))
    with open(path, "w", encoding="utf-8") as file:
        json.dump(d, file)

def sanitize(directory):
    d = getJSON(directory)
    removeInvalid(d, directory)
    removePII(d, directory)
    saveJSON(d, directory)

if __name__ == "__main__":
    sanitize("survey")


