"""
project discription: The aim is to create a small app 
that accept pdf or doc and then create a new file with the same type that
repeat each sentence in the original file as many times as the user wishes 

author: Qiqi Su
"""

""" Import statements """
import tkinter as tk
from tkinter import filedialog as fd
import os
import sys


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

        # create front title
        self.frontmsg = self.canvas.create_text(195, 60, text="Welcome!",
                                                font=("Cursive", 20, "bold"), fill="coral1")

        # create instructional message
        self.instrmsg = self.canvas.create_text(210, 100, text="Please select number of times you wants to repeat here",
                                                font=("Cursive", 10), fill="black")
        self.ormsg = self.canvas.create_text(200, 215, text="Or",
                                             font=("Cursive", 10), fill="black")

        # create spinbox
        # here I set the default value to 4, change it if you wish
        var = tk.StringVar(root)
        var.set("4")
        self.spinbox = tk.Spinbox(
            root, from_=1, to=100, textvariable=var, wrap=True)
        self.spinbox_window = self.canvas.create_window(200, 130, width=50,
                                                        window=self.spinbox)

        # create select pdf file button
        self.select_pdf_btn = tk.Button(root, text="Select PDF file", font=("Times", 15, "bold roman"),
                                        width=20, fg="white", bg="red", command=self.selectpdf)
        self.select_pdf_btn_window = self.canvas.create_window(200, 180, width=250,
                                                               window=self.select_pdf_btn)

        # create select docx file button
        self.select_docx_btn = tk.Button(root, text="Select Docx file", font=("Times", 15, "bold roman"),
                                         width=20, fg="white", bg="red", command=self.selectdocx)
        self.select_docx_btn_window = self.canvas.create_window(200, 250, width=250,
                                                                window=self.select_docx_btn)

    def selectpdf(self):
        file = fd.askopenfile(filetypes=(
            ('PDF files', '*.pdf'), ('All files', '*.*')))

    def selectdocx(self):
        file = fd.askopenfile(filetypes=(
            ('PDF files', '*.pdf'), ('All files', '*.*')))


""" main """
root = tk.Tk()
canvas = SentenceRepeater(master=root)
canvas.mainloop()
