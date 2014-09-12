# using Tkinter's grid() to place widgets
import tkinter as tk
root = tk.Tk()
# create some buttons
button1 = tk.Button(root, text='button1')
button2 = tk.Button(root, text='button2')
button3 = tk.Button(root, text='button3')
# create a label for kicks
label1 = tk.Label(root, text="hello Matty!", fg='red', bg='yellow')
# use a grid to place the buttons
# stay in the same row and add columns
button1.grid(row=0, column=0)
button2.grid(row=0, column=1)
button3.grid(row=0, column=2)
# place the label in the next row
# span across 3 columns, pady (vertical), stretch label horizontally
label1.grid(row=1, column=0, columnspan=3, pady=5, sticky=tk.E+tk.W)
# run the event loop
root.mainloop()
