from pypdf import PdfReader
from pypdf.errors import PdfStreamError
import sys

if len(sys.argv) < 2:
    print("Provide the path of the resume pdf file!")
    print("For example")
    print("python .\\main.py .\\sample_resume\\Resume.pdf")
    exit()

args = sys.argv
file_path = args[1]

try:
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()

    with open("output/resume.txt", "w", encoding="utf8") as f:
        f.write(text)
except FileNotFoundError:
    print("File not found")
except PdfStreamError:
    print("Must be a pdf file")


