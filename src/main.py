from pypdf import PdfReader
from pypdf.errors import PdfStreamError
from collections import Counter
from lib import Words, Phrases
import re
import sys
import json


def main():
    if len(sys.argv) < 3:
        print("Provide the path of the resume pdf file!")
        print("For example")
        print(
            "python src\\main.py sample_resume\\Resume.pdf sample_job_descriptions\\bae_systems_devops_engineer.txt"
        )
        exit()

    args = sys.argv
    resume_file_path = args[1]
    job_description_file_path = args[2]

    convert_resume_pdf_to_text(file_path=resume_file_path)

    json_data = {}

    with open("terms.json", "r", encoding="utf8") as file:
        json_data = json.load(file)

    phrases = json_data["phrases"]
    words = json_data["words"]

    job_text = ""
    with open(job_description_file_path, "r", encoding="utf8") as f:
        job_text = f.read()

    job_text = job_text.lower()

    job_text_words = re.findall(r"\w+", job_text)

    counter_dict_words = {}
    for word in words:
        count = job_text_words.count(word.lower())
        counter_dict_words[word.lower()] = count

    counter_dict_phrases = {}
    for phrase in phrases:
        count = job_text.count(phrase.lower())
        counter_dict_phrases[phrase.lower()] = count

    words_counter = Counter(counter_dict_words)
    phrases_counter = Counter(counter_dict_phrases)

    match_score, words, phrases = get_match_score(
        words_counter, phrases_counter
    )
    match_score = round(match_score, 2)

    print(f"Match Score: {match_score}%\n")
    print(f"Missing words: {words.missing}")
    print(f"Missing phrases: {phrases.missing}\n")
    print(f"Most common words: {words.most_common}")
    print(f"Most common phrases: {phrases.most_common}")


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


def get_match_score(words_counter: Counter, phrases_counter: Counter):
    """Get the match score of the resume"""
    most_common_words = words_counter.most_common(20)
    most_common_phrases = phrases_counter.most_common(20)

    resume_text = ""
    with open("output/resume.txt", "r", encoding="utf8") as f:
        resume_text = f.read()

    resume_text = resume_text.lower()

    num = 0
    total = 0
    missing_words = []
    for count in most_common_words:
        if count[1] > 0:
            total += 2
            if count[0] in resume_text:
                num += 2
            else:
                missing_words.append(count)

    missing_phrases = []
    for count in most_common_phrases:
        if count[1] > 0:
            total += 1
            if count[0] in resume_text:
                num += 1
            else:
                missing_phrases.append(count)

    match_score = 0
    if total != 0:
        match_score = num / total * 100

    words = Words(missing_words, most_common_words)
    phrases = Phrases(missing_phrases, most_common_phrases)

    return match_score, words, phrases


if __name__ == "__main__":
    main()
