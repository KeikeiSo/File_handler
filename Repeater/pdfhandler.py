"""
program discription: group of functions that extract text from pdf,
repeat the sentences, and produce a new pdf

note: change the x and y tolerance and delimiter of sentences if needed

author: Qiqi Su
"""

""" import statement """
import pdfplumber
from pdfplumber.utils import to_list, cluster_objects, collate_line
from collections import defaultdict
import re
import fpdf


""" Gobal variables """
# you should change it if the program does not work properly

# x represent horizontal distance between characters
# y represent vertical distance between characters
# adjust the number for better text extraction from the pdf
DEFAULT_X_TOLERANCE = 2
DEFAULT_Y_TOLERANCE = 3


""" functions """

# return a list of sentences from the pdf


def extract_sentences(
    chars,
    x_tolerance=DEFAULT_X_TOLERANCE,
    y_tolerance=DEFAULT_Y_TOLERANCE,
):
    # preprocess the list of char objects
    chars = to_list(chars)

    if len(chars) == 0:
        return None

    # remove the titles
    # (by only accept most common size chars)
    groups = defaultdict(list)
    for char in chars:
        groups[char["size"]].append(char)

    lists = groups.values()
    content = []
    for l in lists:
        if len(l) > len(content):
            content = l

    # grouping different lines
    doctop_clusters = cluster_objects(content, "doctop", y_tolerance)

    # get each line by joinning the chars into words
    lines = (collate_line(line_chars, x_tolerance)
             for line_chars in doctop_clusters)

    coll = "\n".join(lines)

    sentences = coll.split('.')

    return sentences


# return a string of text with each sentence repeated
def sentence_repeater(text, sentences, frequency):
    context = text.split('.')
    index = 0
    for sentence in sentences:
        if sentence == context[index]:
            sentence = sentence + ".\n"
            to_insert = (frequency - 1) * sentence
            context[index] = to_insert + context[index]
            index += 1
        else:
            x = re.search(sentence, context[index])
            if x:
                sentence = sentence + ".\n"
                to_insert = (frequency - 1) * sentence
                context[index] = context[index][:x.start()] + to_insert + \
                    context[index][x.start():]
                index += 1
            else:
                break
    new_text = '.'.join(context)
    return new_text.replace('\n\n', '\n')


def string_to_pdf(text):
    pdf = fpdf.FPDF(format='letter')  # pdf format
    pdf.add_page()  # create new page
    pdf.set_font("Arial", size=12)  # font and textsize

    line_index = 1
    lines = text.split('\n')
    for line in lines:
        pdf.cell(200, 10, txt=line, ln=line_index, align="C")
        line_index += 1
    pdf.output("test.pdf")


""" main """
pdf = pdfplumber.open(
    "C:/Users/calli/OneDrive/Desktop/(Common Law Library) Hugh Beale - Chitty on Contracts with Second Supplement. I-Sweet & Maxwell (2017).pdf")
page = pdf.pages[0]
text = page.extract_text(x_tolerance=2, y_tolerance=3)
chars = page.chars
sentences = extract_sentences(chars)
print(".".join(sentences))
"""
repeated = sentence_repeater(text, sentences, 2)

pdf.close()

string_to_pdf(repeated)
"""
