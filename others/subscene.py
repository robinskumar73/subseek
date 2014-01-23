import urllib.request as urllib2
import urllib.parse as urlparse 
import os.path,gzip
from io import StringIO
import re
from bs4 import BeautifulSoup

data = urlparse.urlencode({'q':'Finding Neverland (2004)','l':''})
url='http://subscene.com/subtitles/title'
url=url+'?'+data
request = urllib2.Request(url)

#adding headers
request.add_header('Host','subscene.com')
request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0')
request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
request.add_header('Accept-Language','en-US,en;q=0.5')
request.add_header('Connection','keep-alive')
request.add_header('Cache-Control','max-age=0')

s = urllib2.urlopen(request)
soup = BeautifulSoup(s)
print(soup.title)
