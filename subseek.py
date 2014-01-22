
'''
Licence
subSeek 1.0 - Utility software for Microsoft Windows OS designed to be download movies subtitles  files. Copyright (C) 2012 Robins Kumar Gupta This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program; if not, if not, write to the Robins Kumar Gupta Email-robinskumar73@gmail.com For More Info Visit : https://bitbucket.org/robinskumar73/seeksub
'''
#SubSeek Script Created by Robins Gupta
import hashlib
import os
import os.path
import urllib.request as urllib2
import urllib.parse as urlparse,urllib 
import gzip
from io import StringIO
import re
import sys

print('\n\n\n')
print('*'*20 + 'Subtitle Downloaded By Robins Gupta' + '*'*20)
print('\n\n\n')


#Class for creating connection sockets with various subtitle sites
class CreateConn():
    def __init__(self,url,header=None,values=None):
        #returns a connection socket object
        if values:
            #here values must be in dictionary
            data = urlparse.urlencode(values)
        else:
            data=None
        request = urllib2.Request(url,data)

        if header:
            request.add_header('User-Agent',header)

        self.sock_obj = urllib2.urlopen(request) 
    
    def read_data(self,buffer=None):
        #reading data from created socket if data is compressed
        if self.sock_obj.headers['Content-Encoding'] == 'gzip':
            if  buffer:
                data = gzip.GzipFile(fileobj=StringIO(self.sock_obj.read()).read())
            else :
                data = gzip.GzipFile(fileobj=StringIO(self.sock_obj.read()).read(buffer))                
        else:
            if buffer:
                data = self.sock_obj.read(buffer)
            else:
                data = self.sock_obj.read()
        
        #returning the data string
        return data

class SubDb():
    #creating a hash function for retrieving hash name
    def get_md5_hash(self,name):
        read_size = 64 * 1024
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            #Reading first 64 kb of file
            data = f.read(read_size)
            #Now seeking to 64*1024 from last
            f.seek(-read_size, os.SEEK_END)
            #Now reading last 64 kb of file
            data += f.read(read_size)
        #Returning the md5 generated hash function of video file
        return hashlib.md5(data).hexdigest()

    #Now creating a connection with site
    def conn(self,path):
        #we are using a default user-agent provided 
        user_agent = 'SubDB/1.0 (Pyrrot/0.1; http://github.com/jrhames/pyrrot-cli)'
        #creating connecting using GET method
        #getting hash of video file
        hash = self.get_md5_hash(path)
        #creating url of the file
        url = 'http://api.thesubdb.com/?action=download&hash=%s&language=en'%(hash)
        #conn
        try:
            conn = CreateConn(url,header=user_agent)
            if conn.sock_obj.code == 200:
                print('Subtitle  Found \nLanguage:English\n\nDownloading File...')
                #File is downloaded
                #Saving your subtitle
                with open(sub_file(path),'wb') as f:
                    f.write(conn.read_data())
                print ('\nFile Downloaded\nEnjoy!!')
            elif conn.sock_obj.code == 404:
                print (r"File Not Found ")

            elif conn.sock_obj.code == 400:
                print(r"Connection Failed")
            
        except urllib.error.HTTPError:
            print('Sorry!! Subtitle Not Found')
            
        

        
#creating a function for creating the subtitle name
def file_path(path):
    return re.sub(r'(\.mp4|\.avi|\.flv|\.mkv)$','',path)
#creating a function for creating a subtitle file
def sub_file(path):
    return file_path(path)+ u'.srt'

#Now loading the file..
if __name__ == "__main__":
    url_path=sys.argv[1]
    #Now connecting and finding subtitles
    SubDb().conn(url_path)
  
