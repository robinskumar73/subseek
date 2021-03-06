from tkinter import *    # Python 3
from tkinter.ttk import *



class UpdateDialog:
    def __init__(self, title, message):
        #Update dialog box information...
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title(title)
        self.var = StringVar()
        label = Label( self.root, textvariable=self.var, anchor=W, justify=LEFT,text="Helvetica", font=("Helvetica", 14) )
        self.var.set(message)
        label.grid(row=0,pady=5,padx=12)
        button1 = Button(self.root, text="Download", command=self.Ok)
        button2 = Button(self.root, text="Later", command=self.Later)
        button3 = Button(self.root, text="Never Check for updates", command=self.Never)
        # use a grid to place the buttons
        # stay in the same row and add columns
        button1.grid(row=1, column=1,pady=5,padx=10, sticky = S+ N+ E+ W)
        button2.grid(row=1, column=2, pady=5,sticky = W)
        button3.grid(row=1, column=0,pady =5 , padx=5 ,sticky = W+E)
        # place the label in the next row
        # span across 3 columns, pady (vertical), stretch label horizontally
        
            
    def Ok(self):
        self.root.destroy()

    def Later(self):
        self.root.destroy()

    def Never(self):
        self.root.destroy()



def showUpdateDialogBox(title, message):
    app = UpdateDialog(title, message)
    app.root.mainloop()
    
showUpdateDialogBox('Update is avalaible', 'An update is availaible. please download..')
