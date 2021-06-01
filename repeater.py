"""
project discription: The aim is to create a small app 
that accept pdf or doc and then create a new file with the same type that
repeat each sentence in the original file as many times as the user wishes 

author: Qiqi Su
"""

""" Import statements """
import tkinter as tk
from tkinter import filedialog as fd
from pdfhandler import pdf_to_text, get_pages
import os
import pyttsx3


class SentenceRepeater(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # create title
        self.master.title("Sentence Repeater")

        # create canvas
        self.canvas = tk.Canvas(self, bg="white", width=400, height=350)
        self.canvas.pack(fill="both", expand=True)

        # create spinbox
        # here I set the default value to 4, change it if you wish
        var = tk.StringVar(root)
        var.set("4")
        self.spinbox = tk.Spinbox(
            root, from_=1, to=100, textvariable=var, wrap=True)
        

        # create select pdf file button
        self.select_pdf_btn = tk.Button(root, text="Select PDF file", font=("Times", 15, "bold roman"),
                                        width=20, fg="white", bg="red", command=self.selectpdf)

        # create select docx file button
        self.select_docx_btn = tk.Button(root, text="Select Docx file", font=("Times", 15, "bold roman"),
                                         width=20, fg="white", bg="red", command=self.selectdocx)
        
        # create submit button
        self.submit_pdf_btn = tk.Button(root, text="Save as mp3", font=("Times", 15, "bold roman"),
                                         width=20, fg="white", bg="red", command=self.submit_pdf)
        
        # create spinbox of voice gender
        self.gender = tk.StringVar(root)
        self.gender.set("female") # default value
        self.select_gender = tk.OptionMenu(root, self.gender, "female", "male")

    
    def create_front(self):
        # create front title
        self.frontmsg = self.canvas.create_text(195, 80, text="Welcome!",
                                                font=("Cursive", 20, "bold"), fill="coral1")
        # create buttons
        self.select_pdf_btn_window = self.canvas.create_window(200, 160, width=250,
                                                               window=self.select_pdf_btn)
        self.ormsg = self.canvas.create_text(200, 200, text="Or",
                                             font=("Cursive", 10), fill="black")
        self.select_docx_btn_window = self.canvas.create_window(200, 240, width=250,
                                                                window=self.select_docx_btn)

    def selectpdf(self):
        filepath = fd.askopenfilename(filetypes=(
            ('PDF files', '*.pdf'), ('All files', '*.*')))
        if filepath:
            self.open_pdf_gui(filepath)
            return filepath
        else:
            print("File not found")

    def selectdocx(self):
        filepath = fd.askopenfilename(filetypes=(
            ('Docx files', '*.docx'), ('All files', '*.*')))
        if filepath:
            return filepath
        else:
            print("File not found")

    def open_pdf_gui(self, filepath):
        # delete previous stuffs
        self.canvas.delete(self.frontmsg)
        self.canvas.delete(self.select_pdf_btn_window)
        self.canvas.delete(self.ormsg)
        self.canvas.delete(self.select_docx_btn_window)
        # create instructional message
        self.instrmsg = self.canvas.create_text(210, 100, text="Please select number of times you wants to repeat here",
                                                font=("Cursive", 10), fill="black")
        # create spinboc
        self.spinbox_window = self.canvas.create_window(200, 130, width=50,
                                                        window=self.spinbox)
        # message indicating the file that is opened
        self.msg = self.canvas.create_text(210, 50, text="Opened: " + filepath,
                                                font=("Times", 10), fill="gray24")
        
        # from page to page created
        self.pdf_pages = get_pages(filepath)
        num_pages = len(self.pdf_pages)
        begin = tk.StringVar(root)
        begin.set("1")
        self.from_ = tk.Spinbox(root, from_=1, to=num_pages, textvariable=begin, wrap=True)
        end = tk.StringVar(root)
        end.set(str(num_pages))
        self.to = tk.Spinbox(root, from_=1, to=num_pages, textvariable=end, wrap=True)
        self.frommsg = self.canvas.create_text(90, 170, text="From page: ", font=("Cursive", 10), fill="black")
        self.from_window = self.canvas.create_window(150, 170, width=50, window=self.from_)
        self.tomsg = self.canvas.create_text(250, 170, text="To page: ", font=("Cursive", 10), fill="black")
        self.to_window = self.canvas.create_window(300, 170, width=50, window=self.to)

        # select voice gender
        self.vgmsg = self.canvas.create_text(150, 210, text="Please select voice gender: ", \
            font=("Cursive", 10), fill="black")
        self.gender_window = self.canvas.create_window(280, 210, width=80, window=self.select_gender)
        # submit button created
        self.canvas.create_window(200, 270, width=140, window=self.submit_pdf_btn)

    def list_to_text(self, pages):
        content = []
        for page in pages:
            content.append('\n'.join(page))
        text = '\n'.join(content)
        return text
    
    def submit_pdf(self):
        curr_directory = os.getcwd() # will get current working directory
        output = fd.asksaveasfilename(initialdir = curr_directory,\
            title = "Select file",filetypes = (("mp3 files","*.mp3"),("all files","*.*")))
        start = int(self.from_.get()) - 1
        end = int(self.to.get()) 
        freq = int(self.spinbox.get())
        pages = pdf_to_text(self.pdf_pages, start, end, freq)
        text = self.list_to_text(pages)
        
        # text to voice
        engine = pyttsx3.init() # object creation
        voices = engine.getProperty('voices')       #getting details of current voice
        if self.gender.get() == "female":
            engine.setProperty('voice', voices[1].id)
        else:
            engine.setProperty('voice', voices[0].id)
        
        engine.save_to_file(text, output)
        engine.runAndWait()
        return



""" main """
root = tk.Tk()
canvas = SentenceRepeater(master=root)
canvas.create_front()
canvas.mainloop()
