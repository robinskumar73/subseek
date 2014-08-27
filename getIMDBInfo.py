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
        conn = opensubtitle.OpenSubtitle(url_path,'robinskumar73','subseek2014',True)
        #Search for subtitle in opensubtitle.org
        results = conn.SearchSubtitles()
        if results:
            
            #Download subtitle
            #Now checking for data in result...
            data = results
            movieName = data['title']
            year = data['year']
            movie_genre = ''
            plot = data['plot']
            
            
            if data['genres']:
                for genre in data['genres']:
                    if movie_genre == '':
                        movie_genre = movie_genre + '' + genre
                    else:
                        movie_genre = movie_genre +  " | " + genre
                    
            rating =   data['rating']
            #Now showing info...
            display("IMDB INFO.", " Movie Name: " + movieName  + "\n Rating: " + rating + "\n\n Year release: " + year + "\n Genre: " + movie_genre +"\n\n Plot:  " + plot + "..." )
            
            #Now closing session from opensubtitles
            'Logging out from opensubtitle server'
            conn.logout()
                    
                
                    

        else:
            #Now closing session from opensubtitles
            conn.logout()
            
            display("Sorry movie info not found","Sorry movie info not found")


    except socket.gaierror:
            display("Unable to connect to the internet", "Check your internet connection.")

    except:
        display("Sorry movie info not found","Sorry movie info not found.")
