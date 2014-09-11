try:
  import Tkinter              # Python 2
  import ttk
except ImportError:
  import tkinter as Tkinter   # Python 3
  import tkinter.ttk as ttk
 
 
def main():
 
  root = Tkinter.Tk()
 
  ft = ttk.Frame()
 
  ft.pack(expand=False, fill=Tkinter.BOTH, side=Tkinter.TOP)

  pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='determinate',length='20')
 
  pb_hd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
  pb_hd.step(50)

 
  root.mainloop()
 
 
if __name__ == '__main__':
  main()
  print("Now opening the file downloaded succesfully..")
