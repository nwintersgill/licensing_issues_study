
import csv, os

questions = ("D3","C1","C2","C3","C4",
             "C6","C7","E2","E4","E6",
             "EC1","EC3","EC5","N2",
             "N3","N4","N6")         # Coded questions
pid_filter = []                      # User IDs to ignore
# coders = 3                           # The number of coders
input_file_template = "coder_%d.csv" # Format of the coded file names
output_file = "diff_locations.csv"   # Name of the output file
diff_file = "diffs.csv"              # Name of the diffs file

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

def makeComparison(codes):
    lyst = []
    for pid in codes[0].keys():
        for question in questions:
            coder_1 = codes[0][pid].get(question, None)
            if all(coder_1 == coder[pid].get(question, None) for coder in codes):
                if not int(pid) in pid_filter:
                    lyst.append((pid, question))
    return lyst

def getDiffs(codes, pid, question):
    lists = [code[pid][question] for code in codes]

    all_elements = set(item for sublist in lists for item in sublist)
    elements_not_in_all = []

    for element in all_elements:
        count = sum(1 for sublist in lists if element in sublist)
        if count < len(lists):
            elements_not_in_all.append(element)

    return elements_not_in_all

def writeDiffs(codes, matches):
    path = os.path.join("generated_files", diff_file)
    with open(path, "w", encoding="utf-8") as file:
        file.write("," + ",".join(questions) + "\n")
        for pid in codes[0].keys():
            file.write(pid + ",")
            for q in questions:
                if (pid, q) in matches:
                    file.write("[],")
                else:
                    diffs = getDiffs(codes, pid, q)
                    diffs = '"' + str(diffs) + '"'
                    file.write(diffs+",")
            file.write("\n")
        file.flush()

def saveToFile(codes, matches):
    path = os.path.join("generated_files", output_file)
    with open(path, "w", encoding="utf-8") as file:
        file.write("," + ",".join(questions) + "\n")
        for pid in codes[0].keys():
            file.write(pid + ",")
            for q in questions:
                if (pid, q) in matches:
                    file.write(",")
                else:
                    file.write("X,")
            file.write("\n")
        file.flush()

def main(coders):
    codes = readCodeFiles(coders)
    matches = makeComparison(codes)
    saveToFile(codes, matches)
    writeDiffs(codes, matches)

if __name__ == "__main__":
    main()





