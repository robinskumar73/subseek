from tkinter import *    # Python 3
from tkinter.ttk import *
from update import *
from bs4 import *
import multiprocessing
import os
from subseek import *





class UpdateDialog:
    def __init__(self, title, message):
        #Update dialog box information...
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title(title)
        self.var = StringVar()
        #self.temp = temp
        label = Label( self.root, textvariable=self.var,  justify=LEFT,text="Helvetica", font=("Helvetica", 14) )
        self.var.set(message)
        label.grid(row=0,pady=5,padx=12)
        button1 = Button(self.root, text="Download", command=self.Ok)
        button2 = Button(self.root, text="Later", command=self.Later)
        button3 = Button(self.root, text="Never Check for updates", command=self.Never)
        # use a grid to place the buttons
        # stay in the same row and add columns
        button1.grid(row=2, column=0,pady=5,padx=10,sticky =W+E)
        button2.grid(row=2, column=1, pady=5,padx=10,sticky =W)
        button3.grid(row=1, column=0,pady =5 ,padx=10, sticky =W+E)
        # place the label in the next row
        # span across 3 columns, pady (vertical), stretch label horizontally
        
            
    def Ok(self):
        #self.root.withdraw()
       
        p = multiprocessing.Process(target=runUpdate_)
        p.daemon = False
        p.start()
            
        print("I am existing...from updateDialog module")
        #Now destroying the dialog
        self.root.destroy()
        

    def Later(self):
        self.root.destroy()


    def Never(self):
        #Write new configuration file
        #getting file location..
        data = '''<?xml version="1.0" encoding="utf-8"?>\n<subseeek>\n '''
         
        #getting file location..
        dir_ = getAppPath()
        file = os.path.join(dir_, "configuration.xml")
        f = open(file,'r')
        handler = f.read()
        f.close()
        soup = BeautifulSoup(handler)
        #file = "E:\\subseek_new\configuration.xml"
        data = data + str(soup.subtitlelanguage)
        data = data + ' \n<updateCheck>\n0\n</updateCheck>\n</subseeek>'
        with open(file,'w') as f:
            f.write(data)
        #Now destroy the dialog box and exit...
        self.root.destroy()



def showUpdateDialogBox(title, message):
    app = UpdateDialog(title, message)
    app.root.mainloop()
    
if __name__ == '__main__':
    showUpdateDialogBox('Update is avalaible', 'An update is availaible. please download..')
   
