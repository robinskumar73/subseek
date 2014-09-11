from tkinter import *    # Python 3
from tkinter.ttk import *
import urllib.request as urllib2
import os 
import threading
import socket
import time



class MyTkApp(threading.Thread):
    
    def __init__(self, url):
        
        self.url = url
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title("Downloading Subseek update..")
        self.var = StringVar()
        photo = PhotoImage(file="file_download.png")
        w = Label(self.root, image=photo)
        w.photo = photo
        w.pack()
    
        label = Label( self.root, textvariable=self.var, anchor=W, justify=LEFT,text="Helvetica", font=("Helvetica", 14) )
        self.var.set("Downloading subseek update...    0% done")
        label.pack()
    
        self.pb_hd = Progressbar(self.root, orient='horizontal', mode='indeterminate',length=300) 
        self.pb_hd.pack(expand=False, fill=BOTH, side=TOP)
        
        threading.Thread.__init__(self)
        
        

    def run(self):
        
        #Now connecting to download ...
        
        url = self.url
        file_name = url.split('/')[-1]
        print(url)
        try:
            self.var.set("Connecting to server....")
            u = urllib2.urlopen(url)
            print('Got connected..')
            f = open(file_name, 'wb')
            file_size = int(u.headers['Content-Length'])
            self.pb_hd.maximum = file_size
            file_size_dl = 0
            block_sz = 8192
            initialValue = 0
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%3.2f%%" % ( file_size_dl * 100. / file_size)
                self.var.set("Downloading subseek update...    %s done" %(status))
                
            #closing of file..
            f.close()

            
        except socket.gaierror:
            self.var.set("Error unable to connect to internet..     ")
            self.root.title("Check your internet connection..       ")
            time.sleep(2)
            self.root.title("Existing..     ")
            time.sleep(1)
            self.root.destroy()

        except ConnectionAbortedError:
            self.var.set("Error established connection aborted..      ")
            self.root.title("Connection aborted..           ")
            time.sleep(2)
            self.root.title("Existing..        ")
            time.sleep(1)
            self.root.destroy()
            
        except RuntimeError:
            #delete the file here... occurs on force exit..
            print('closed..')
            



 
 
if __name__ == '__main__':
  app = MyTkApp('https://github.com/robinskumar73/subseek/releases/download/v1.3/setup.zip')
  app.start()
  app.root.mainloop()
  print("Now opening the file downloaded succesfully..")
