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


print('\n\n\n')
print('*'*20 + 'Subtitle Downloaded By Robins Gupta' + '*'*20)
print('\n\n\n')



#Writing subtitle to file...
def write(path,data):
    with open(path,'wb') as f:
        f.write(data)



#Now loading the file..
if __name__ == "__main__":
    #Commenting temporarilly
    url_path=sys.argv[1]
    #url_path = "E:\\No Smoking 2007.avi"
    
    #f_err = open("err_log.log", "w")
    #sys.stdout = f_err
    #Subtitle file name
    sub_file_name = subdb.sub_file(url_path)
    
    #First try subtitle from opensubtitle....
    print('Connecting to openSubtitle...')
    try:
        print("I am here in main file")
        conn = opensubtitle.OpenSubtitle(url_path,'robinskumar73','subseek2014')
        #Search for subtitle in opensubtitle.org
        results = conn.SearchSubtitles()
        
        if results:
            #Download subtitle
            #Now checking for data in result...
            for data in results:
                try:
                    download_link = data['SubDownloadLink']
                    if download_link:
                        request = urllib2.Request(download_link)
                        request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201')
                        sock_obj = urllib2.urlopen(request)
                        f=BytesIO(sock_obj.read())
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

    except:
        #Try Connecting to SubDb....
        print('connecting to subdb server')
        try:
            subdb.SubDb().conn(url_path)
        except FileNotFoundError:
            display("Sorry, File not found", "Subtitle not found.")
            
      
        
    #Closing std-err file..
    #f_err.close()
    
