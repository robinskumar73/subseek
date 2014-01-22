import sys
from cx_Freeze import setup, Executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "subSeek",
        version = "1.1",
        description = "Downloads Movies Subtitle",
        #options = {"build_exe":{'init_script':'C:\\Users\\Robins\\Desktop\\subseek\\registry.py'}} ,
        executables = [Executable("subseek.py", base=base)])
