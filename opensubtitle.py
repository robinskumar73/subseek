import urllib.request as urllib2
import urllib.parse as urlparse 
import os.path,gzip
from io import StringIO
import re
from bs4 import BeautifulSoup
import struct
import xmlrpc.client as xmlrpclib
#SubSeek Script Created by Robins Gupta
import hashlib
import os
import os.path
import gzip
import zlib



class OpenSubtitle:
      'Class for searching and downloading subtitle from OpenSubtitle'

      def __init__(self,path,user,pass_):
            'Contructor for opensubtitle'
            'Connecting to server'
            self.proxy = xmlrpclib.ServerProxy('http://api.opensubtitles.org/xml-rpc')
            #Login
            self._login(user,pass_)
            self.path=path
            print('Login Successfull...')
            #gathering movie data..
            #Checking Movie By hash
            data = hashFile(self.path)
            self.FileSize = data[1]
            self.movie_hash = data[0]
            #Checking the Movie file information
            self.movie_info = self.check_movie_hash(self.movie_hash)
            
            
      def _login(self,username,password):
            resp = self.proxy.LogIn(username, password, 'en', 'OS Test User Agent')
            self.check_status(resp)
            self.token = resp['token']
            
      def SearchSubtitles(self):
            'Method for searching subtitles'
            sublanguageid = 'eng'
            'Getting MovieHash...'
            if self.path:
                  
                  query = os.path.basename( file_path(self.path) )

                  #Creating a request ...
                  if self.movie_info:
                        req = [ {'sublanguageid': sublanguageid, 'moviehash': str(self.movie_hash), 'moviebytesize': str(self.FileSize), \
                                 'imdbid': self.MovieImdbID,'query': str(query), 'season':self.SeriesSeason, 'episode':self.SeriesEpisode, 'tag':'0' } ]
                  else:
                        req = [ {'sublanguageid':'eng','query': str(query)} ]
                        
                  resp = self.proxy.SearchSubtitles(self.token,req)
            else:
                  print("Path not defined")
 
                  
      
      #Exception handling part
      def check_status(self,response):
            if response['status'].upper() != '200 OK' :
                  print(response['status'].upper())
                  return False
            else:
                  return True

      def check_movie_hash(self,moviehash):
            response = self.proxy.CheckMovieHash(self.token,[moviehash])
            if self.check_status(response):
                  #Return the data...
                  data=response['data'][moviehash]
                  if data:
                        self.MovieYear = data['MovieYear']
                        self.SeriesEpisode = data['SeriesEpisode']
                        self.SeriesSeason = data['SeriesSeason']
                        self.MovieHash = data['MovieHash']
                        self.MovieName = data['MovieName']
                        self.MovieKind = data['MovieKind']
                        self.MovieImdbID = data['MovieImdbID']
                        #return data
                        movie_info = (self.MovieYear, self.SeriesEpisode, self.SeriesSeason, self.MovieHash, self.MovieName, self.MovieKind, self.MovieImdbID)
                        return movie_info
                        
                  else:
                        #Ignore these
                        return ()
                        
                  
                        
            else:
                  raise Exception('Error response from server response code: ' + response['status'].upper())
            
            

#creating a function for creating the subtitle name
def file_path(path):
    return re.sub(r'(\.mp4|\.avi|\.flv|\.mkv)$','',path)

#Hash function for generating files..
def hashFile(name): 
      try: 
                 
                longlongformat = 'q'  # long long 
                bytesize = struct.calcsize(longlongformat) 
                    
                f = open(name, "rb") 
                    
                filesize = os.path.getsize(name) 
                hash = filesize 
                    
                if filesize < 65536 * 2: 
                       return "SizeError" 
                 
                for x in range(int(65536/bytesize)): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
                         
    
                f.seek(max(0,filesize-65536),0) 
                for x in range(int(65536/bytesize)): 
                        buffer = f.read(bytesize) 
                        (l_value,)= struct.unpack(longlongformat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF 
                 
                f.close() 
                returnedhash =  "%016x" % hash
                'Return tuple'
                hash_data = (returnedhash,filesize)
                return  hash_data
    
      except(IOError): 
                return "IOError"
def get_md5_hash(name):
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













