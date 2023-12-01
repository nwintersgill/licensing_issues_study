
import csv, json, os
from itertools import combinations

questions = ("D3","C1","C2","C3","C4",
             "C6","C7","E2","E4","E6",
             "EC1","EC3","EC5","N2",
             "N3","N4","N6")         # Coded questions
pid_filter = []                      # User IDs to ignore
# coders = 3                           # The number of coders
input_file_template = "coder_%d.csv" # Format of the coded file names
output_file = "response_codes.json"         # Name of the output file


def readCSVFile(path):
    d = {}
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i > 0:
                pid = row[0]
                if pid.strip() != "" and not int(pid) in pid_filter:
                    d[pid] = {}
                    for j, column in enumerate(questions):
                        codes = row[j+2].strip()
                        if codes == "":
                            codes = "[]"
                        d[pid][column] = set(eval(codes))
    return d

def readCodeFiles(coders):
    codes = []
    for x in range(coders):
        path = input_file_template % (x+1,)
        path = os.path.join("code_files", path)
        codes.append(readCSVFile(path))
    return codes

def createFormattedJSON(coders):
    d = {}
    for q in questions:
        d[q] = {}
        for pid in coders[0].keys():
            d[q][pid] = {}
            for i, coder in enumerate(coders):
                d[q][pid][f"R{i}"] = list(coder[pid][q])
    return d

def all_combinations(input_list):
    all_combinations_list = []
    for r in range(1, len(input_list) + 1):
        all_combinations_list.extend(combinations(input_list, r))
    return ["".join(combo) for combo in all_combinations_list]

def addCodeToLabel(d, code, label):
    if label in d:
        d[label].append(code)
    else:
        d[label] = [code]

def getAllCodes(coders):
    all_codes = []
    for coder in coders:
        all_codes.extend(coder)
    return set(all_codes)

def addLabels(d, coders):
    labels = all_combinations([f"R{i}" for i in range(len(coders))])
    for label in labels:
        d[label] = []

def main(coders):
    coders = readCodeFiles(coders)
    d = createFormattedJSON(coders)

    # Create unique JSON (conveys more information)
    uniques = {}
    ids = coders[0].keys()

    for q in questions:
        uniques[q] = {}

        for pid in ids:

            responses = {}

            # Get all codes for the question
            coders = d[q][pid].values()
            addLabels(responses, coders)
            all_codes = getAllCodes(coders)

            # Determine who used each code (the label)
            for code in all_codes:
                label = ""
                for i, coder in enumerate(coders):
                    if code in coder:
                        label += f"R{i}"
                addCodeToLabel(responses, code, label)

            uniques[q][pid] = responses

    path = os.path.join("generated_files", output_file)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(uniques, file)

if __name__ == "__main__":
    main()

