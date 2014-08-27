import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["opensubtitle","subdb","hashlib","xmlrpc.client","struct",\
"os","re","urllib.request","urllib.parse","gzip","sys","io","tkinter","messagebox","getIMDBInfo"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "subseek",
        version = "1.1",
        description = "One Click Movie subtitle downloader",
        options = {"build_exe": build_exe_options},
        executables = [Executable("subseek.py", base=base),
                       Executable("getIMDBInfo.py", base=base)]
    )
