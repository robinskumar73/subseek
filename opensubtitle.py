import os.path
import re
import struct
import xmlrpc.client as xmlrpclib
#SubSeek Script Created by Robins Gupta
import hashlib
import os
import os.path




class OpenSubtitle:
      'Class for searching and downloading subtitle from OpenSubtitle'

      def __init__(self,path,user,pass_):
            'Contructor for opensubtitle'
            'Connecting to server'
            self.proxy = xmlrpclib.ServerProxy('http://api.opensubtitles.org/xml-rpc')
            #Login
            self._login(user,pass_)
            self.path=path
            print('Login Successfull to openSubtitle...')
            #gathering movie data..
            #Checking Movie By hash
            self.data = hashFile(self.path)
            self.FileSize = self.data[1]
            self.movie_hash = self.data[0]
            #Checking the Movie file information
            self.movie_info = self.check_movie_hash(self.movie_hash)
            
            
      def _login(self,username,password):
            resp = self.proxy.LogIn(username, password, 'en', 'OS Test User Agent')
            self.check_status(resp)
            self.token = resp['token']

      def search_imdb(self,name):
            #Modify name using regex
            #Converting '-' and '.' in space chr
            name = re.sub(r'(\-|\.)',' ',name)
            resp = self.proxy.SearchMoviesOnIMDB(self.token,name)
            print('IMDB SEARCH...')
            if self.check_status(resp):
                  'return the most expected movie id and the newly formed query in tuple'
                  return (resp['data'][0],name)
             
            
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
                        #Check for imdb availaible info...
                        file_info = self.search_imdb(query)
                        query = file_info[1]
                        self.MovieImdbID = file_info[0]['id']
                        req = [ {'sublanguageid':sublanguageid, 'moviebytesize': str(self.FileSize), 'imdbid': self.MovieImdbID, 'query': str(query)} ]
                          
                  resp = self.proxy.SearchSubtitles(self.token,req)
                  
                  #Checking for response
                  if self.check_status(resp):
                        return resp['data']
                  else:
                        return False
                        
            else:
                  print("Path not defined")
 
                  
      
      #Exception handling part
      def check_status(self,response):
            if response['status'].upper() != '200 OK' :
                  print(response['status'].upper())
                  return False
            else:
                  return True
      def logout(self):
            self.proxy.LogOut(self.token)

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



