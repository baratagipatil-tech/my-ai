from pypdf import PdfReader

pdf_path = "Class_9_Maths_Master_Solutions_With_Formulas.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    text += page.extract_text() + "\n"

print(text)