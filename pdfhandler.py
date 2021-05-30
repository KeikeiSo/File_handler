"""
program discription: group of functions that extract text from pdf,
repeat the sentences, and produce a new pdf

note: change the x and y tolerance if extraction produces error

author: Qiqi Su
"""

""" import statement """
import pdfplumber
from pdfplumber.utils import to_list, cluster_objects, collate_line
from collections import defaultdict
import re
import fpdf
import nltk.data


""" Gobal variables """
# you should change it if the program does not work properly

# x represent horizontal distance between characters
# y represent vertical distance between characters
# adjust the number for better text extraction from the pdf
DEFAULT_X_TOLERANCE = 2
DEFAULT_Y_TOLERANCE = 3
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


""" functions """

# return a list of sentences from the pdf


def extract_sentences(
    page,
    x_tolerance=DEFAULT_X_TOLERANCE,
    y_tolerance=DEFAULT_Y_TOLERANCE,
):
    # preprocess the list of char objects
    chars = page.chars
    chars = to_list(chars)

    if len(chars) == 0:
        return None

    # remove the titles
    # (by only accept most common size chars)
    groups = defaultdict(list)
    # only get characters above the line if there is one
    delimiter = 0
    for line in page.lines:
        if line["linewidth"] >= 1:
            delimiter = line["top"]
    if delimiter != 0:
        for char in chars:
            if char["bottom"] < delimiter:
                groups[char["size"]].append(char)
    else:
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

    coll = coll.replace('!', '.').replace('?', '.')
    
    sentences = tokenizer.tokenize(coll)

    return sentences

# helper function for sentence_repeater
# return the starting index (-1 if not found)
def search_sentence(str1, str2):
    try:
        x = re.search(str1, str2)
        if x:
            return x.start()
        else:
            s = str1.split(",")
            y = re.search(s[0], str2)
            if y:
                return y.start()
            else:
                return -1
    except Exception:
        s = str1.split(",")
        y = re.search(s[0], str2)
        if y:
            return y.start()
        else:
            return -1

# return a string of text with each sentence repeated
def sentence_repeater(text, sentences, frequency):
    text = text.replace('!', '.').replace('?', '.')
    context = tokenizer.tokenize(text)
    
    """
    text_file = open("C:/Users/calli/OneDrive/Desktop/text.txt", "w")
    context = [sentence.replace('\n', ' ').replace('  ', ' ') for sentence in context]
    text_file.write("\n".join(context))
    text_file.close()

    text_file = open("C:/Users/calli/OneDrive/Desktop/sentences.txt", "w")
    sentences = [sentence.replace('\n', ' ').replace('  ', ' ') for sentence in sentences]
    text_file.write("\n".join(sentences))
    text_file.close()
    """
    
    index = 0

    # find the place first sentence match
    indicator = sentences[0]
    while (index < len(context) - 1):
        if indicator == context[index]:
            break
        else:
            if search_sentence(indicator, context[index]) == -1:
                index += 1
            else: 
                break
    # repeat each sentence and add them back
    for sentence in sentences:
        if sentence == context[index]:
            to_insert = sentence.replace('\n', ' ')
            to_insert = frequency * to_insert
            context[index] = to_insert
            index += 1
        else:
            start = search_sentence(sentence, context[index])
            if start != -1:
                to_insert = sentence.replace('\n', ' ')
                to_insert = frequency * to_insert
                context[index] = context[index][:start] + to_insert \
                    + context[index][start + len(sentence):]
                index += 1
            else:
                break

    new_text = " ".join(context)

    # getting rid of special character that cannot be printed to pdf by fpdf
    new_text = new_text.replace('“', '\"').replace('”', '\"')
    new_text = new_text.replace('‘', "\'").replace('’', "\'")
    new_text = new_text.replace('—', '--').replace('–', '-')
    new_text = new_text.replace('©', 'copyright_')
    
    return new_text.replace('\n\n', '\n')

def split_for(str, pos):
    t = len(str) // pos
    for i in range(t):
        d = pos*(i+1)
        while(str[d] != " "):
            d += 1
            if d >= len(str)-1:
                break
        str = str[:d] + "\n" + str[d:]
    return str

def trim_text(text, pos):
    new_lines = []
    lines = text.split('\n')
    for line in lines:
        new_lines.append(split_for(line, pos))
    return "\n".join(new_lines)

def pdf_repeater(filepath, start, end, frequency, new_filepath, font_size=12):
    
    pdf = pdfplumber.open(filepath)

    new_pdf = fpdf.FPDF(format='letter')
    new_pdf.set_font("Arial", size=font_size)
    new_pdf.add_page()

    pages = pdf.pages[start:end]
    for page in pages:
        text = page.extract_text(x_tolerance=2, y_tolerance=3)
        sentences = extract_sentences(page)
        """
        text_file = open("C:/Users/calli/OneDrive/Desktop/testing.txt", "w")
        sentences = [sentence.replace('\n', ' ') for sentence in sentences]
        text_file.write("\n".join(sentences))
        text_file.close()
        """
        repeated = sentence_repeater(text, sentences, frequency)
        new_text = trim_text(repeated, 90)

        line_index = 1
        lines = new_text.split('\n')
        for line in lines:
            new_pdf.cell(200, 10, txt=line, ln=line_index, align="C")
            line_index += 1

    new_pdf.output(new_filepath)

    new_pdf.close()
    pdf.close()
    
""" main """
if __name__ == '__main__':
    """
    pdf = pdfplumber.open(
        "C:/Users/calli/OneDrive/Desktop/Contract Law (Macmillan Law Mas - Ewan McKendrick.pdf")
    page = pdf.pages[88]
    text = page.extract_text(x_tolerance=2, y_tolerance=3)

    sentences = extract_sentences(page)

    repeated = sentence_repeater(text, sentences, 2)

    text_file = open("C:/Users/calli/OneDrive/Desktop/sample.txt", "w")
    text_file.write(repeated)
    text_file.close()

    string_to_pdf(repeated)
    pdf.close()
    """
    pdf_repeater("C:/Users/calli/OneDrive/Desktop/LA1040_VLE.pdf", 
    12, 13, 2, "C:/Users/calli/OneDrive/Desktop/testing.pdf", font_size=12)

