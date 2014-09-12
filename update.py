from tkinter import *    # Python 3
from tkinter.ttk import *
import urllib.request as urllib2
import os 
import threading
import socket
from  time import sleep
#for creating a temporary folder
from tempfile import mkdtemp
from subseek import *
import sys











url = 'https://github.com/robinskumar73/subseek/releases/download/v1.3/setup.exe'

class MyTkApp(threading.Thread):
    
    def __init__(self, url):

        
        self.url = url
        self.temp = mkdtemp()
        print(self.temp)
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title("Downloading Subseek update..")
        self.var = StringVar()
        #getting file location..
        dir_ = getInstalledPath(GetAppID())
        path = os.path.join(dir_, 'file_download.png' )
        print(path)
        photo = PhotoImage(file=path)
        w = Label(self.root, image=photo)
        w.photo = photo
        w.pack()
        label = Label( self.root, textvariable=self.var, anchor=W, justify=LEFT,text="Helvetica", font=("Helvetica", 14) )
        label.pack(anchor=W, pady=8, padx=5)
    
        self.pb_hd = Progressbar(self.root, orient='horizontal', mode='indeterminate',length=400) 
        #self.pb_hd.pack(expand=False, fill=BOTH, side=TOP, pady = 0)
        #self.pb_hd.start()
        threading.Thread.__init__(self)
        self.daemon = True
        
        

    def run(self):
        
        #Now connecting to download ...
        
        url = self.url
        file_name = url.split('/')[-1]
        print(url)
        try:
            self.path = os.path.join(self.temp,file_name)
            self.var.set("Connecting to server....")
            u = urllib2.urlopen(url)
            print('Got connected..')
            print(self.path)
            f = open(self.path, 'wb')
            file_size = int(u.headers['Content-Length'])
            f.truncate(file_size)
            #self.pb_hd.maximum = file_size
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
                self.var.set("Downloading subseek update.    %s done" %(status))
                
            print("Now opening the file downloaded succesfully..")
            f.flush()
            print("Now closing the file..")
            f.close()
            sleep(2)
            print("Opening downloaded file..")
            os.startfile(self.path)
            self.root.destroy()
            
                
            

            
        except socket.gaierror:
            self.var.set("Error unable to connect to internet..     ")
            self.root.title("Check your internet connection..       ")
            sleep(2)
            self.root.title("Existing..     ")
            sleep(1)
            self.root.destroy()
           

        except ConnectionAbortedError:
            self.var.set("Error established connection aborted..      ")
            self.root.title("Connection aborted..           ")
            sleep(2)
            self.root.title("Existing..        ")
            sleep(1)
            self.root.destroy()
            

            
        except RuntimeError:
            #delete the file here... occurs on force exit..
            print('closed..')

        except:
            pass

        finally:
            #closing of dialog..
            self.root.destroy()
            sys.exit()
           
           
def runUpdate_():
    app_ = MyTkApp(url)
    app_.start()
    app_.root.mainloop()


 
 
if __name__ == '__main__':
    runUpdate_()
 
  
