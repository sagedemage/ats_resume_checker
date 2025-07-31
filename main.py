from pypdf import PdfReader
from pypdf.errors import PdfStreamError
import sys
import json
from collections import Counter
import re

def main():
    if len(sys.argv) < 2:
        print("Provide the path of the resume pdf file!")
        print("For example")
        print("python .\\main.py .\\sample_resume\\Resume.pdf")
        exit()

    args = sys.argv
    file_path = args[1]

    convert_resume_pdf_to_text(file_path=file_path)

    json_data = {}

    with open("terms.json", "r", encoding="utf8") as file:
        json_data = json.load(file)

    phrases = json_data["phrases"]
    words = json_data["words"]

    job_text = ""
    with open("job_description/job_description.txt", "r", encoding="utf8") as f:
        job_text = f.read()

    job_text = job_text.lower()

    job_text_words = re.findall(r'\w+', job_text)

    counter_dict = {}
    for phrase in phrases:
        count = job_text.count(phrase.lower())
        counter_dict[phrase.lower()] = count

    for word in words:
        count = job_text_words.count(word.lower())
        counter_dict[word.lower()] = count

    counter = Counter(counter_dict)

    match_score, missing_terms, most_common = get_match_score(counter)

    print(f"Match Score: {match_score}%")
    print(f"Missing terms: {missing_terms}")
    print(f"Most common terms: {most_common}")

def convert_resume_pdf_to_text(file_path: str):
    """Convert a resume pdf file to a text file"""
    try:
        reader = PdfReader(file_path)
        page = reader.pages[0]
        text = page.extract_text()

        with open("output/resume.txt", "w", encoding="utf8") as f:
            f.write(text)
    except FileNotFoundError:
        print("File not found")
    except PdfStreamError:
        print("Must be a pdf file")

def get_match_score(counter: Counter):
    """Get the match score the resume"""
    most_common = counter.most_common(20)

    resume_text = ""
    with open("output/resume.txt", "r", encoding="utf8") as f:
        resume_text = f.read()

    resume_text = resume_text.lower()

    num = 0
    total = 0
    missing_terms = []
    for count in most_common:
        if count[1] > 0:
            total += 1
            if count[0] in resume_text:
                num += 1
            else:
                missing_terms.append(count)

    match_score = num/total * 100
    return match_score, missing_terms, most_common

if __name__== "__main__":
    main()
