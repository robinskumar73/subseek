import tkinter as tk
from tkinter import messagebox as mb


def messagebox(title, label):
    root = tk.Tk()
    root.withdraw()
    mb.showinfo(title, label)
 


if __name__ == '__main__':
    import multiprocessing
    #Now Displaying an Exception Frame Asking for Giving Destination action
    p = multiprocessing.Process(target=messagebox,args=('ACTION','',))
    p.daemon = False
    p.start()
    print("BYE BYE")


