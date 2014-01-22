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
                  for data in resp['data']:
                        match_result = re.match( r'([A-Za-z0-9()\[\]]*)[\s|\.|\-|=]*([A-Za-z0-9()\[\]]*)?[\s|\.|\-|=]*([A-Za-z0-9()\[\]]*)?[\s|\.|\-|=]*', data['title'])
                        #Checking for match query..
                        print(match_result.group(1).lower())
                        if (not name.lower().find(match_result.group(1).lower()) == -1 and \
                            ( not name.lower().find(match_result.group(2).lower()) == -1 or not name.lower().find(match_result.group(3).lower()) == -1 )):
                              #Matching occurs return data
                              print ('\nMatched data')
                              print(data)
                              return (data,name)
                        else:
                              continue
            
      def SearchSubtitles(self):
            'Method for searching subtitles'
            sublanguageid = 'eng'
            'Getting MovieHash...'
            if self.path:
                  
                  query = os.path.basename( file_path(self.path) )
                  #Creating a request ...
                  #Preparing request
                  request_query = {'sublanguageid': sublanguageid, 'moviebytesize': str(self.FileSize),'tag':'0'}
                  if self.MovieHash:
                        #Adding hash to request_query
                        request_query['moviehash']=self.MovieHash
                        #Adding query
                        request_query['query'] = str(query)
                        print('printing movie hash')
                        
                  if not self.MovieImdbID:
                        print('searching for imdb id')
                        file_info = self.search_imdb(query)
                        query = file_info[1]
                        self.MovieImdbID = file_info[0]['id']
                        #Now adding imdb id..
                        request_query['imdbid'] = self.MovieImdbID
                        #Adding query
                        request_query['query'] = str(query)
                  else:
                        #Now adding imdb id..
                        request_query['imdbid'] = self.MovieImdbID
                        
                  if self.SeriesSeason and not self.SeriesSeason == '0':
                        request_query['season'] = self.SeriesSeason
                        request_query['episode'] = self.SeriesEpisode
                        
                  request = []
                  #appending query to request list
                  request.append(request_query)
                  print('\nrequest is: \n')
                  print(request)        
                  resp = self.proxy.SearchSubtitles(self.token,request)
                  print('\nresponse is: \n')
                  
                  #Checking for response
                  if self.check_status(resp) and resp['data']:
                        return resp['data']
                  else:
                        #Search without using movie hash..
                        del request_query['moviehash']
                        print(request_query)
                        #Now search Once More
                        resp = self.proxy.SearchSubtitles(self.token,request)
                        print(resp['data'][0])
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
                  
                  
                  if response['data'] and response['data'][moviehash]:
                        #Return the data...
                        data=response['data'][moviehash]
                        self.MovieYear = data['MovieYear']
                        self.SeriesEpisode = data['SeriesEpisode']
                        self.SeriesSeason = data['SeriesSeason']
                        self.MovieHash = data['MovieHash']
                        self.MovieName = data['MovieName']
                        self.MovieKind = data['MovieKind']
                        self.MovieImdbID = data['MovieImdbID']            
                        
                  else:
                        self.MovieYear = ""
                        self.SeriesEpisode = ""
                        self.SeriesSeason = ""
                        self.MovieHash = ""
                        self.MovieName = ""
                        self.MovieKind = ""
                        self.MovieImdbID = ""

                  #return data
                  movie_info = (self.MovieYear, self.SeriesEpisode, self.SeriesSeason, self.MovieHash, self.MovieName, self.MovieKind, self.MovieImdbID)
                  return movie_info
                  
                        
            else:
                  raise Exception('Error response from server response code: ' + response['status'].upper())
            
#Creating exception class...
class MyException(Exception):
      def imdbIdError(self):
            pass
      
      def seriesIdError(self):
            pass
      
      def episodeIdError(self):
            pass
      
      def MovieHashError(self):
            pass

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



