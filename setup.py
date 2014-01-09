import sys
from cx_Freeze import setup, Executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "subSeek",
        version = "0.1",
        description = "Download Movies Subtitle",
        #options = {"build_exe":{'init_script':'Console'}} 
        executables = [Executable("subseek.py", base=base)])
