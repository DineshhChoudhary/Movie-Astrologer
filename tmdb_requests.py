import requests
import json


class requestsTmdb:

    def __init__(self):
        self.APIKey="b126f5fe06990a5ed0ca90867b2251b3"
        self.baseurl="https://api.themoviedb.org/3/"

    def search(self,movieName):
        url=self.baseurl+"search/movie/?api_key="+self.APIKey+"&language=en-US&query="+movieName
        resp=requests.get(url)
        data=json.loads(resp.content)
        for result in data["results"]:
            return result
    def popular(self,region=""):
        url="https://api.themoviedb.org/3/movie/popular?api_key=b126f5fe06990a5ed0ca90867b2251b3&language=en-US&page=1"
        if region!="":
            url=url+"&region="+region
        resp=requests.get(url)
        data=json.loads(resp.content)
        return data
    def topRatedMovies(self,region=""):
        url="https://api.themoviedb.org/3/movie/top_rated?api_key=b126f5fe06990a5ed0ca90867b2251b3&language=en-US&page=1"
        if region!="":
            url=url+"&region="+region
        resp=requests.get(url)
        data=json.loads(resp.content)
        return data
    def upcomingMovies(self,region=""):
        url="https://api.themoviedb.org/3/movie/upcoming?api_key=b126f5fe06990a5ed0ca90867b2251b3&language=en-US&page=1"
        if region!="":
            url=url+"&region="+region
        resp=requests.get(url)
        data=json.loads(resp.content)
        return data

    def movieCast(self,movieID):
        url="https://api.themoviedb.org/3/movie/"+str(movieID)+"/credits?api_key=b126f5fe06990a5ed0ca90867b2251b3"
        resp=requests.get(url)
        data=json.loads(resp.content)
        for character in data['cast']:
            return data
    def recommendedMovies(self,movieID):
        url="https://api.themoviedb.org/3/movie/"+movieID+"/recommendations?api_key=b126f5fe06990a5ed0ca90867b2251b3&language=en-US&page=1"
        resp=requests.get(url)
        data=json.loads(resp.content)
        return data
    def similarMovies(self,movieID):
        url="https://api.themoviedb.org/3/movie/"+movieID+"/similar?api_key=b126f5fe06990a5ed0ca90867b2251b3&language=en-US&page=1"
        resp=requests.get(url)
        data=json.loads(resp.content)
        return data

    def getGenreIDName(self):
        url="https://api.themoviedb.org/3/genre/movie/list?api_key=b126f5fe06990a5ed0ca90867b2251b3&language=en-US"
        resp=requests.get(url)
        data=json.loads(resp.content)
        return data

    def findByImdbID(self,imdbID):
        url="https://api.themoviedb.org/3/find/"+ImdbID+"?api_key=b126f5fe06990a5ed0ca90867b2251b3&language=en-US&external_source=imdb_id"
        resp=requests.get(url)
        data=json.loads(resp.content)
        return data







