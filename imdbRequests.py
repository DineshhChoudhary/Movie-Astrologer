from bs4 import BeautifulSoup
import webbrowser
import urllib
import requests
import re

#http://image.tmdb.org/t/p/w185//7PIBDIQPMuFzMPvCFUgxhM842f0.jpg
class imdbRequest:

    def __init__(self):
        self.movieName=""
        self.baseUrl="http://www.imdb.com"
        self.url="http://m.imdb.com/find?q="
        self.urlCopy="http://m.imdb.com/find?q="
        self.imdbRating=10
        self.imdbID=""
        self.imdbName=""
        
    def requestImdb(self,movieName):
        self.url=self.urlCopy+movieName
        soup=BeautifulSoup(requests.get(self.url).content,'lxml')
        tag=soup.find(href=re.compile("/title/tt.*"))
        self.imdbid=tag['href'][7:-1]
        self.imdbName=tag.string
        colon=":"
        if colon in self.imdbName:
            self.imdbName=self.imdbName.replace(colon," ")
        soup=BeautifulSoup(requests.get(self.baseUrl+tag['href']).content,'lxml')
        self.imdbRating=soup.strong.span.string
        
    def getimdbID(self):
        return self.imdbID
    def getimdbRating(self):
        return self.imdbRating
    def getimdbName(self):
        return self.imdbName
    
        
'''     

movie=
base_url='http://www.imdb.com'
url='http://m.imdb.com/find?q='+movie
soup=BeautifulSoup(requests.get(url).content,'lxml')
tag=soup.find(href=re.compile("/title/tt.*"))
print(tag.string)
soup=BeautifulSoup(requests.get(base_url+tag['href']).content,'lxml')
print(soup.strong.span.string)
title=soup.findAll("td","title")
for t in title:
    print(t.find("h1").contents[0].strip())

#print(soup.findAll('h3'))
#print(soup.meta['content'])

if desc['property']=='description':
    print(desc.property)

'''

