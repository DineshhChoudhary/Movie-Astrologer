import requests
import json

class Movietmdb:

    def __init__(self):
        self.title=""
        self.language=""
        self.director=""
        self.duration=""
        self.adult=""
        self.overview=""
        self.imdbRating=10.0
        self.id=0 
        self.poster_path=""
        self.backdrop_path=""
        self.release_date=""
        self.crew=[]
        self.genre_id=[]

    def getTitle(self):
        return self.title
    def getYear(self):
        return self.year
    def getLanguage(self):
        return self.language
    def getDirector(self):
        return self.director
    def getId(self):
        return self.id
    def getAdult(self):
        return self.adult
    def getimdbRating(self):
        return self.imdbRating
    def setimdbRating(self,rating):
        self.imdbRating=rating
    def getOverview(self):
        return self.overview
    def getPosterPath(self):
        return self.poster_path
    def getBackdropPath(self):
        return self.backdrop_path
    def getReleaseDate(self):
        return release_date

    def getResults(self):
        data=[]
        data.append(self.id)
        data.append(self.imdbRating)
        data.append(self.title)
        data.append(self.language)
        data.append(self.adult)
        data.append(self.overview)
        data.append(self.poster_path)
        data.append(self.backdrop_path)
        data.append(self.release_date)
        return data

    def getGenreList(self):
        return self.genre_id
        
    def setResults(self,data):
        self.id=data["id"]
        self.title=data["title"]
        colon=":"
        while colon in self.title:
            self.title=self.title.replace(colon,"")
        self.year=data["release_date"]
        self.poster_path=data["poster_path"]
        self.backdrop_path=data["backdrop_path"]
        self.language=data["original_language"]
        #self.duration=str(data["runtime"])
        self.adult=data["adult"]
        self.overview=data["overview"]
        self.release_date=data["release_date"]
        self.genre_id=[]
        for id in data["genre_ids"]:
            self.genre_id.append(id)
        
        
'''

url="https://api.themoviedb.org/3/search/movie?api_key=b126f5fe06990a5ed0ca90867b2251b3&language=en-US&query=titanic"
#soup=BeautifulSoup(requests.get(url).content,'lxml')
#print(soup.find("title"))

url="https://api.themoviedb.org/3/find/tt4849438?api_key=b126f5fe06990a5ed0ca90867b2251b3&language=en-US&external_source=imdb_id"
resp=requests.get(url)
data=json.loads(resp.content)
for result in data["movie_results"]:
    print(result)

r=requests.get(url)
data=json.loads(r.content)
for result in data["results"]:
    print(result)
    break
'''
