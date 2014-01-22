import urllib.request as urllib2
import urllib.parse as urlparse 
import os.path,gzip
from io import StringIO
import re
from bs4 import BeautifulSoup

data = urlparse.urlencode({'api_key':'004c76c9eedfbf2061f7538e0cdc189173af81c5','q':'Finding.Neverland','gzip':'off','search_in':'releases'})
url='http://api.subtitleseeker.com/search/?'
url=url + data
request = urllib2.Request(url)


request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0')
request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
request.add_header('Accept-Language','en-US,en;q=0.5')
request.add_header('Connection','keep-alive')
request.add_header('Cache-Control','max-age=0')

s = urllib2.urlopen(request)
soup = BeautifulSoup(s)

#Now checking for results..
#getting the title name..
title_name='Finding.Neverland'
#Now checking for matched title_name in first search string only...


    
        
        
        
