
import openpyxl, json, os

questions = ("D3","C1","C2","C3","C4",
             "C6","C7","E2","E4","E6",
             "EC1","EC3","EC5","N2",
             "N3","N4","N6") 

dictionary_file = 'dictionary.xlsx'
output_file = 'glossary.json'

def main():
    # Load the Excel file
    in_path = os.path.join('code_files', dictionary_file)
    workbook = openpyxl.load_workbook(in_path)

    # Select the sheet you want to work with
    sheet = workbook['Selection Options']

    def getDefinition(comment):
        if comment is None:
            return ("", "")
        else:
            comment = comment.text.split('\n\t-')
            return (comment[0], comment[-1])
        
    # Iterate over columns
    terms = {}
    for i, column in enumerate(sheet.iter_cols(min_col=1, max_col=17, min_row=3)):
        terms[questions[i]] ={}
        for cell in column:
            term = cell.value
            definition, author = getDefinition(cell.comment)
            if term != None:
                terms[questions[i]][term] = definition

    out_path = os.path.join("generated_files", output_file)
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(terms, file)

if __name__ == "__main__":
    main()