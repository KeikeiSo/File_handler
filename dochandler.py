"""
program discription: group of functions that read the doc,
repeat the sentences and produce a new doc

author: Qiqi Su
"""

""" import statement """
from docx import Document
import nltk.data

def doc_repeater(filepath, frequency, new_filepath):
    document = Document(filepath)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    
    for paragraph in document.paragraphs:
        sentences = tokenizer.tokenize(paragraph.text)
        new_sentences = []
        for sentence in sentences:
            sentence = sentence + " "
            sentence = sentence * frequency
            new_sentences.append(sentence)
        paragraph.text = " ".join(new_sentences)
    document.save(new_filepath)

""" main """
if __name__ == '__main__':
    doc_repeater('C:/Users/calli/OneDrive/Desktop/GLJ-Notes-Manual-2019.docx',\
    2, 'C:/Users/calli/OneDrive/Desktop/sample2.docx')