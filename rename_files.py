from os import walk
import os
from imdbRequests import imdbRequest
from tmdb_requests import requestsTmdb
from tmdb_api import Movietmdb
from dbMovie import MovieDatabase

class renameFiles:

    def __init__(self):
        self.replace1 = [ "english","hindi","fmovies.to",".avi","1.4","5.1","-","DVDRip","BRRip","XviD","1CDRip","aXXo","[","]","(",")","{","}","{{","}}"
        "x264","x265","720p","StyLishSaLH (StyLish Release)","DvDScr","MP3","HDRip","WebRip",
        "ETRG","YIFY","StyLishSaLH","StyLish Release","TrippleAudio","EngHindiIndonesian",
        "385MB","CooL GuY","a2zRG","x264","Hindi","AAC","PSK","CyBorG","AC3","MP3"," R6","HDRip","H264","ESub","AQOS",
        "ALLiANCE","UNRATED","ExtraTorrentRG","BrRip","mkv","mpg","DiAMOND","UsaBitcom","AMIABLE",
        "BRRIP","XVID","AbSurdiTy","DVDRiP","TASTE","BluRay","HR","COCAIN","_",".","BestDivX","MAXSPEED",
        "Eng","500MB","FXG","Ac3","Feel","Subs","S4A","BDRip","FTW","Xvid","Noir","1337x","ReVoTT",
        "GlowGaze","mp4","Unrated","hdrip","ARCHiViST","TheWretched","www","torrentfive","com",
        "1080p","1080","SecretMyth","Kingdom","Release","RISES","DvDrip","ViP3R","RISES","BiDA","READNFO",
        "HELLRAZ0R","tots","BeStDivX","UsaBit","FASM","NeroZ","576p","LiMiTED","Series","ExtraTorrent","DVDRIP","~",
        "BRRiP","699MB","700MB","greenbud","B89","480p","AMX","007","DVDrip","h264","phrax","ENG","TODE","LiNE",
        "XVid","sC0rp","PTpower","OSCARS","DXVA","MXMG","3LT0N","TiTAN","4PlayHD","HQ","HDRiP","MoH","MP4","BadMeetsEvil",
        "XViD","3Li","PTpOWeR","3D","HSBS","CC","RiPS","WEBRip","R5","PSiG","'GokU61","GB","GokU61",
        "PSEUDO","DVD","Rip","NeRoZ","EXTENDED","DVDScr","xvid","WarrLord","SCREAM","MERRY","XMAS","iMB","7o9",
        "Exclusive","171","DiDee","v2","WEB","DL","Worldfree4u","ind in","trade","1Gb","Movie",
        "Dual","Mafiaking","M2Tv","DD","Audio","lish"," 5 1+    5 1","Pre","DvDRip","DvD","dvd","pDvD",
        "bid","trade","HDTV","HEVC","HC","800mb"," dd"," 5 1+ 5 1  ","800Mb","Esub","worldfree4u",
        "827MB","Clean","ShAaNiG","Dubbed"," by ","Filmywap","HD","Dub","In","Scr",
        "Downloadhub","9xmovies","Dvdrip","AmirFarooqi","YouTube","MKV","SaM","avi", 
        " MaNuDiL","SilverRG","2CH","PSA","fmovies.to","fmovies","Bluray","filmxy","849 MB"
        ]
        self.folderPath=[]
        self.moviePathList={}
        self.currDir=os.curdir
        self.numberOfFiles=0

    def getMoviePathList(self):
        return self.moviePathList
    
    def setFolderPath(self,path):
        for p in path:
            self.folderPath.append(p[0])

    def walkDirectories(self):
        for p in self.folderPath:
            for(dirpath,dirnames,filenames) in os.walk(p):
                for file in filenames:
                    if os.path.getsize(os.path.join(dirpath,file))>10**8:
                        self.moviePathList[file]=dirpath
                        self.numberOfFiles=self.numberOfFiles+1
                                   
    def requestImdb(self):
        imdbreq=imdbRequest()
        tmdbreq=requestsTmdb()
        tmdbresults=Movietmdb()
        dbmovie=MovieDatabase()
        
        dbmovie.dbcreate()#create database
        lookuppath=dbmovie.dbExecuteQuery('select moviepath from path')
        #set path
        self.setFolderPath(lookuppath)
        self.walkDirectories()
        #for r in tmdbreq.getGenreIDName():
        dbmovie.dbinsertGenreDetails(tmdbreq.getGenreIDName())
        for file,path in self.moviePathList.items():
            try:
                    
                old_name=file
                dot="."
                while dot in old_name:
                    old_name=old_name.replace(dot," ")
                
                for value in self.replace1:
                    old_name=old_name.replace(value," ")
                for i in range(1900,2027):
                    if str(i) in old_name:
                        old_name=old_name.replace(str(i),"")
                print(old_name)
                imdbreq.requestImdb(old_name)
                tmdbresults.setResults(tmdbreq.search(imdbreq.getimdbName()))
                tmdbresults.setimdbRating(imdbreq.getimdbRating())
                #rename file
                #try:
                if os.path.exists(os.path.join(path,file)):
                    print(os.path.join(path,file))
                else:
                    print("no",os.path.join(path,file))
                print(os.path.join(path,imdbreq.getimdbName()+os.path.splitext(file)[1]))
                os.rename(os.path.join(path,file),os.path.join(path,imdbreq.getimdbName()+os.path.splitext(file)[1]))
                #except:
                    #print("Renaming error")
                if not dbmovie.isPresent(tmdbresults.getId()):
                    dbmovie.dbinsertMovieDetails(tmdbresults.getResults())
                    dbmovie.dbinsertMovieGenre(tmdbresults.getId(),tmdbresults.getGenreList())
                    dbmovie.dbsetMovieLocation(imdbreq.getimdbName(),path,os.path.splitext(file)[1])
                    dbmovie.dbsetMovieCast(tmdbresults.getId(),tmdbreq.movieCast(tmdbresults.getId()))
                    dbmovie.dbcommit()
            except TypeError:
                print("File name Error")
                print("Enter the correct name of the following file Left Blank to pass")
                print(old_name)
                input_movie_name=input()
                if input_movie_name=="":
                    continue
                imdbreq.requestImdb(input_movie_name)
                tmdbresults.setResults(tmdbreq.search(imdbreq.getimdbName()))
                tmdbresults.setimdbRating(imdbreq.getimdbRating())
                #rename file
                try:
                    os.rename(os.path.join(path,file),os.path.join(path,imdbreq.getimdbName()+os.path.splitext(file)[1]))
                except:
                    print("Renaming error")

                if not dbmovie.isPresent(tmdbresults.getId()):
                    dbmovie.dbinsertMovieDetails(tmdbresults.getResults())
                    dbmovie.dbinsertMovieGenre(tmdbresults.getId(),tmdbresults.getGenreList())
                    dbmovie.dbsetMovieLocation(imdbreq.getimdbName(),path,os.path.splitext(file)[1])
                    dbmovie.dbsetMovieCast(tmdbresults.getId(),tmdbreq.movieCast(tmdbresults.getId()))
                    dbmovie.dbcommit()
                
        dbmovie.dbCloseConnection()

'''       
t=renameFiles()
#t.setFolderPath("G:/movies")

#t.walkDirectories()
t.requestImdb()
'''
