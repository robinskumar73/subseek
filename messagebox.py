import tkinter as tk
from tkinter import messagebox as mb


def messagebox(title, label):
    root = tk.Tk()
    root.withdraw()
    mb.showinfo(title, label)


