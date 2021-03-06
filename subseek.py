import sys
import subdb
import opensubtitle 
import gzip
import urllib.request as urllib2
from io import BytesIO
import re
import zipfile
import socket
from messagebox import messagebox as display
from bs4 import *
import os
from updateDialog import *
#Python code for reading registry information...
from winreg import ConnectRegistry, OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE
from multiprocessing import freeze_support

    







#----DEFINING SOME GLOBAL VALUES UPDATE WHEN GENERATING ITS SETUP EVERTIME----
def GetAppID():
    #Unique appId for subseek in registry
    return '{79BD0AB7-300D-4434-AB0A-04BFD868DB4B}_is1'



#Writing subtitle to file...
def write(path,data):
    with open(path,'wb') as f:
        f.write(data)

def getLanguage():
    #getting file location..
    dir_ = getAppPath()
    file = os.path.join(dir_, "configuration.xml")
    #file = "E:\\subseek_new\configuration.xml"
    try:
        handler = open(file).read()
    except FileNotFoundError:
        #Create a dummy configuration file...
        data = '''<?xml version="1.0" encoding="utf-8"?>
<subseeek>
 <subtitlelanguage>
eng
</subtitlelanguage> 
<updateCheck>
1
</updateCheck>
</subseeek>'''

        try:
            with open(file,'w') as f:
                f.write(data)
            handler = open(file).read()
            
        except:
            #In this case fall back to english subtitles...
            return 'eng'
            
    soup = BeautifulSoup(handler)
    try:
        m = re.search('[a-zA-Z0-9]+', soup.subtitlelanguage.contents[0])
        return m.group(0)
    except:
        return 'eng'


def getCheckUpdatePermission():
    #getting file location..
    dir_ = getAppPath()
    file = os.path.join(dir_, "configuration.xml")
    
    handler = open(file).read()
    soup = BeautifulSoup(handler)
    try:
        m = re.search('[0-9]+', soup.updatecheck.contents[0])
        return m.group(0)
    except:
        return 1
    
def getUrlData(url, decodeUTF_8 = False):
    request = urllib2.Request(url)
    request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201')
    sock_obj = urllib2.urlopen(request)
    if decodeUTF_8:    
        data = sock_obj.read()
        data = data.decode("utf-8")
    else:
        data = sock_obj.read()
    return data


def GetSubseekRegistryVersion(AppID):
    #returns the installed subseek version info..
    """ Reading from SOFTWARE\Microsoft\Windows\CurrentVersion\Run  """
    aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    abs_path = os.path.join(path, AppID)
    aKey = OpenKey(aReg, abs_path)
    val = QueryValueEx(aKey, "DisplayVersion")
    val = float(val[0])
    return val


def getInstalledPath(AppID):
    #returns the installed subseek version info..
    """ Reading from SOFTWARE\Microsoft\Windows\CurrentVersion\Run  """
    aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    abs_path = os.path.join(path, AppID)
    aKey = OpenKey(aReg, abs_path)
    val = QueryValueEx(aKey, "InstallLocation")
    val = val[0]
    return val

def getAppPath():
    path = os.getenv('APPDATA')
    abs_path = os.path.join(path,"Subseek")
    if(os.path.exists(abs_path)):
        return abs_path
    else:
        os.makedirs(abs_path)
    return abs_path
    

#Now loading the file..
if __name__ == "__main__":

    print('\n\n\n')
    print('*'*20 + 'Subtitle Downloaded By Robins Gupta' + '*'*20)
    print('\n\n\n')

    
    try:
        freeze_support()
    except:
        sys.exit()
    #Commenting temporarilly
    url_path=sys.argv[1]
    #url_path="D:\\Kiss Kiss Bang Bang BRRrip 720p x264 Dual Audio[Eng-Hindi] -=rAhuLKO=-more on www.mastitorrents.com.mkv"
    
    
    #f_err = open("err_log.log", "w")
    #sys.stdout = f_err
    #Subtitle file name
    sub_file_name = subdb.sub_file(url_path)
    
    #First try subtitle from opensubtitle....
    print('Connecting to openSubtitle...')
    try:
        
        conn = opensubtitle.OpenSubtitle(url_path,'robinskumar73','subseek2014',False,getLanguage())
        print("Connection created to opensubtutle..") 
        #Search for subtitle in opensubtitle.org
        results = conn.SearchSubtitles()
        
        if results:
            #Download subtitle
            #Now checking for data in result...
            for data in results:
                try:
                    download_link = data['SubDownloadLink']
                    if download_link:
                        f=BytesIO(getUrlData(download_link))
                        data = gzip.open(f).read()
                        
                        #Now writing subtitle to file...
                        write(sub_file_name, data)
                        print ('subtitle downloaded successfully...Enjoy!!')
                        
                        break
                       
                    
                except KeyError:
                    print('Downloading a zip file')
                    try:
                        download_link = data['ZipDownloadLink']
                    except:
                        'If no key exists for zipdownload then continue'
                        continue
                    
                    #Connecting to server...
                    if download_link:
                        request = urllib2.Request(download_link)
                        request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201')
                        sock_obj = urllib2.urlopen(request)
                        f=BytesIO(sock_obj.read())
                        if zipfile.is_zipfile(f):
                            #Creating a zipfile object
                            z=zipfile.ZipFile(f, mode='r')
                            sub_file=[]
                            for file in z.namelist():
                                matchObj = re.match( r'(.*srt$)', file)
                                if matchObj:
                                    #Appending all subtitle files to list
                                    sub_file.append(file)

                            #Writing zip file
                            if sub_file and len(sub_file)==1:
                                data = z.read(sub_file[0])
                                #Now writing subtitle to file...
                                sub_data = write(sub_file_name, data)
                                
                            else:
                                print('extracting all zip files')
                                z.extractall()

                            print('Subtitle downloaded enjoy!!\n')
                        else:
                            'Given zip file is not valid continue searching for others subtitles'
                            continue
                        #Now breaking the loop
                        break
                    
                    
            #Now closing session from opensubtitles
            'Logging out from opensubtitle server'
            conn.logout()
            
        else:
            #Now closing session from opensubtitles
            conn.logout()
            raise Exception('Subtitle not found in opensubtitle database')

    except socket.gaierror:
            display("Unable to connect to the internet", "Check your internet connection.")
            sys.exit()

    except:
        #Try Connecting to SubDb....
        print('connecting to subdb server')
        try:
            lang = getLanguage()
            lang = lang[0] + lang[1]
            subdb.SubDb().conn(url_path, lang)
        except FileNotFoundError:
            display("Sorry, File not found", "Subtitle not found.")
            sys.exit()
        except:
            display("Error could connect","Could create connection to the server. Check your internet connection.")
            sys.exit()
    #---------------------------------------------SCRIPT FOR CHECKING OF UPDATES---------------------------------
    '''NOW CHECKING FOR UPDATES IF AVAILAIBLE...'''
    #checking first if  update is permissible or not...
    if getCheckUpdatePermission() == '1':
        print("I am checking for permission....")
        #Get current version value from the server..
        VersionLink = "http://subseek.in/version.txt"
        try:
            data = getUrlData(VersionLink, True)
        except:
            display("Unable to connect to the internet", "Check your internet connection.")
            sys.exit()
        #formatting the data to get the exact version info.  
        Version = re.sub(r"[a-z]*", '', data, flags=re.IGNORECASE)
        Version = float(Version)
        #Now checking this value from our window registry installed version..
        appId = GetAppID()
        #Now getting the installed version info of registry...
        InstalledVersion = GetSubseekRegistryVersion(appId)
     
        if Version > InstalledVersion:
            #An update is found...
            '''Display a message box showing an update is found..'''
            title = "Update availaible for version " + str(Version)
            message = "An update for subseek is availaible for version " + str(Version) + "."
            #Creating a TEMP FOLDER..
            #for creating a temporary folder
            showUpdateDialogBox(title, message )
            
          
        
    
