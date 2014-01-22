import winreg

#Creating a registry file for software..
key=winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,"*\\shell",0, winreg.KEY_ALL_ACCESS)
key_folder=winreg.CreateKey(key, "SubSeek")
winreg.SetValue(key,"SubSeek",winreg.REG_SZ,"Download Subtitle")
command_key=winreg.CreateKey(key_folder,"command")
key_folder=winreg.OpenKey(key,"SubSeek",0, winreg.KEY_ALL_ACCESS)

winreg.SetValue(key_folder,"command",winreg.REG_SZ, "\"C:\\Program Files\\subSeek\\subseek.exe\" \"%1\"")
