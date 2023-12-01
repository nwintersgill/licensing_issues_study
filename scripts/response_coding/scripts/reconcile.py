
import csv, copy, os

pid_filter = []
questions = ("D3","C1","C2","C3","C4",
             "C6","C7","E2","E4","E6",
             "EC1","EC3","EC5","N2",
             "N3","N4","N6") 

base_name = "coder_1.csv"
fixed_name = "reconciliation.csv"
output_name = "final_coding.csv"

def main():
    
    path = os.path.join("code_files", base_name)
    base = readCSVFile(path)

    path = os.path.join("code_files", fixed_name)
    fixed = readCSVFile(path)

    combined = combine(base, fixed)
    path = os.path.join("generated_files", output_name)
    writeToFile(combined, path)

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
                        if codes != "":
                            d[pid][column] = eval(codes)
    return d

def combine(d1, d2):
    d3 = copy.deepcopy(d1)
    for pid in d1.keys():
        for question in questions:
            if d2[pid].get(question, False):
                d3[pid][question] = d2[pid][question]
            elif d1[pid].get(question, False):
                d3[pid][question] = d1[pid][question]
    return d3

def writeToFile(d, fileName):
    with open(fileName, "w", encoding="utf-8") as file:
        file.write("," + ",".join(questions) + "\n")
        for pid in d.keys():
            file.write(pid + ",")
            for i, q in enumerate(questions):
                if d[pid].get(q, False):
                    resp = d[pid][q]
                    file.write('"' + str(resp) + '"')
                if i < len(questions) - 1:
                    file.write(",")
            file.write("\n")
        file.flush()

if __name__ == "__main__":
    main()
