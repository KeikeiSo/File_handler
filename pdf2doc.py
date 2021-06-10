import argparse
from sys import int_info
from pdfhandler import get_pages, pdf_to_endocx
import os

# required input arguments 
"""
input file: -i input
output file: -o output
number of times to repeat: -n freq
page number from which it reads: from_
page number until which it reads: to
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A program that mulplicates sentences \
        in the pdf n times then produces a docx file')
    parser.add_argument('input', metavar='input', type=str, help='Input pdf filepath')
    parser.add_argument('--o', type=str, \
        default='nameless.docx', help='Output docx filepath')
    parser.add_argument('--n', type=int, \
        default=4, help='number of times to repeat')
    parser.add_argument('--f', type=int, \
        default=1, help='from which page you want to include')
    parser.add_argument('--t', type=int, \
        default=1, help='until which page you want to include')
    args = parser.parse_args()

    print("Processing input...")
    path = os.path.abspath(args.input)
    if os.path.exists(path):
        pages = get_pages(path)
        print("Input file is: ", os.path.basename(path), " with number of pages: ", len(pages))
        pdf_to_endocx(pages, args.f-1, args.t, args.n, args.o)
    else:
        print("The file does not exist.")


