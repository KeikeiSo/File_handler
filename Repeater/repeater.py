"""
project discription: The aim is to create a small app 
that repeat sentence in a file as many times as the user wishes

author: Qiqi Su
"""

""" Import statements """
import tkinter as tk
from PIL import ImageTk, Image
import os
import sys


class SentenceRepeater(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # create title and icon
        self.master.title("Sentence Repeater")

        # create canvas
        self.canvas = tk.Canvas(self, bg="white", width=400, height=300)
        self.canvas.pack(fill="both", expand=True)


""" main """
root = tk.Tk()
canvas = SentenceRepeater(master=root)
canvas.mainloop()
