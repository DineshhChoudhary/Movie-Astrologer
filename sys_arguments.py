import getopt,sys,os
from rename_files import renameFiles
from imdbRequests import imdbRequest
from tmdb_requests import requestsTmdb
from tmdb_api import Movietmdb
from dbMovie import MovieDatabase

def system_arguments():
    try:
        opts,args=getopt.getopt(sys.argv[1:],"h",["help","imdb=","refresh","path","top=","date=","watched","add_to_watched=","remove_from_watched=",
                                                  "remove_from_path=","add_to_path=","favorites","add_to_favorites=","remove_from_favorites=",
                                                  "play=","cast=","overview=","download_subtitle="])
    except:
        usage()
    dbmovie=MovieDatabase()
    dbmovie.dbcreate()
    for o,a in opts:
        if o=="-h":
            usage()
        elif o=="--help":
            usage()
        elif o=="--imdb":
            result=dbmovie.dbExecuteQuery("select title,imdbrating from moviedetails order by imdbrating desc")
            nor=0#number of results
            
            for res in result:
                if a!="all" and nor>int(a):
                    break
                nor=nor+1
                print(str(res[1]),end='')
                print("\t",str(res[0]))
        elif o=="--top":
            result=dbmovie.dbExecuteQuery("select imdbrating,title,id from moviedetails  order by imdbrating desc limit '%s'" %a)
            nor=0#number of results
            resultlist=[]
            for res in result:
                resultlist.append(res)
                            
            for res in resultlist:
                if a!="all" and nor>int(a):
                    break
                nor=nor+1
                print(str(res[0]),end='')
                print("\t",str(res[1]))
                
                print("\t\t\t\t\t\t",end='')
                #genreresult=dbmovie.dbExecuteQuery("select genrename from genredetails left join moviegenre on genredetails.genreid=moviegenre.genreid where id='%s'" %int(res[3]))
                genreresult=dbmovie.dbExecuteQuery("select genrename from genredetails where genreid in (select distinct mg.genreid from moviegenre as mg where mg.id=%i)" %(int(res[2])))
                genre=""
                for r in genreresult:
                    genre+=r[0]
                    genre+=","
                print(genre[:-1])
        
        #elif o=="--rename":
        elif o=="--refresh":
            fileRename=renameFiles()
            fileRename.requestImdb()
        elif o=="--path":
            result=dbmovie.dbExecuteQuery("select moviepath from path")
            print("all paths are:")
            for r in result:
                print(r[0])
        elif o=="--add_to_path":
            if os.path.exists(str(a)):                
                dbmovie.dbAddPath(str(a))
                dbmovie.dbcommit()
                result=dbmovie.dbExecuteQuery("select moviepath from path")
                print("all paths are:")
                for r in result:
                    print(r[0])
            else :
                print("path doesn't exists")
        elif o=="--remove_from_path":
            print(a)
            dbmovie.dbRemovePath(a)
            dbmovie.dbcommit()
            result=dbmovie.dbExecuteQuery("select moviepath from path")
            print("all paths are:")
            for r in result:
                print(r[0])
                
        elif o=="--date":
            result=dbmovie.dbExecuteQuery("select imdbrating,release_date,title,id from moviedetails order by release_date desc")
            nor=0#number of results
            resultlist=[]
            for res in result:
                resultlist.append(res)
                            
            for res in resultlist:
                if a!="all" and nor>int(a):
                    break
                nor=nor+1
                print(str(res[0]),end='')
                print("\t",str(res[1]),end='')
                print("\t",str(res[2]))
                print("\t\t\t\t\t\t",end='')
                #genreresult=dbmovie.dbExecuteQuery("select genrename from genredetails left join moviegenre on genredetails.genreid=moviegenre.genreid where id='%s'" %int(res[3]))
                genreresult=dbmovie.dbExecuteQuery("select genrename from genredetails where genreid in (select distinct mg.genreid from moviegenre as mg where mg.id=%i)" %(int(res[3])))
                genre=""
                for r in genreresult:
                    genre+=r[0]
                    genre+=","
                print(genre[:-1])
                
        elif o=="--watched":
            result=dbmovie.dbExecuteQuery("select title from watched")
            for r in result:
                print(r[0])
            print("")
        elif o=="--add_to_watched":
            result=dbmovie.dbExecuteQuery("select id,title from moviedetails where title='%s'" %a)
            for r in result:
                dbmovie.dbinsertToWatched(r)
            dbmovie.dbcommit()
        elif o=="--remove_from_watched":
            dbmovie.dbremoveFromWatched(a)
            dbmovie.dbcommit()
            print(a,"deleted from watched")

        elif o=="--favorites":
            result=dbmovie.dbExecuteQuery("select title from favorites")
            for r in result:
                print(r[0])
            print("")
        elif o=="--add_to_favorites":
            result=dbmovie.dbExecuteQuery("select id,title from moviedetails where title='%s'" %a)
            for r in result:
                dbmovie.dbinsertToFavorites(r)
            dbmovie.dbcommit()
        elif o=="--remove_from_favorites":
            dbmovie.dbremoveFromFavorites(a)
            dbmovie.dbcommit()
            print(a,"deleted from favorites")
        elif o=="--play":
            result=dbmovie.dbgetMovieLocation(a)
            fullpath=result[0]+"\\"+a+result[1]
            os.startfile(fullpath)
        elif o=="--download_subtitle":
            result=dbmovie.dbgetMovieLocation(a)
            fullpath=result[0]+"\\"+a+result[1]
            download_subtitle(result[0],a)
            
        elif o=="--overview":
            result=dbmovie.dbExecuteQuery("select title,imdbrating,adult,language,overview,release_date from moviedetails where title='%s'" %a)
            for r in result:
                print("Title:________",r[0])
                print("Imdb:_________",r[1])
                print("Adult:________",r[2])
                print("Language:_____",r[3])
                print("Release Date:_",r[5])
                print("Overview:_____",r[4])

        elif o=="--cast":
            movieid=dbmovie.dbExecuteQuery("select id from moviedetails where title='%s'" %a)
            for id in movieid:
                moviecast=dbmovie.dbgetMovieCast(id)
                for cast in moviecast:
                    print(cast[0]+"    as    "+cast[1])
        

def usage():
    print("following are the options:")
    print("-h or --help --------------------for help")
    print("--top [n] -----------------------to display top n movies")
    print("--imdb [all || n] ---------------to display all or top n results sorted by imdb")
    print("--refresh -----------------------to refresh list")
    print("--path  -------------------------Added paths ")
    print("--add_to_path [path]-------------to add path ")
    print("--remove_from_path [path] -------to remove 'path' from path")
    print("--date [all || n] ---------------to list all or top n movies sorted by date" )
    print("--watched  ----------------------to display watched movies")
    print("--add_to_watched [exact movie name]----------to add movies to watched")
    print("--remove_from_watched [exact movie name]-----to remove movies from watched")
    print("--date [all || n] ---------------------------to display top n or all movies sorted by date")
    print("--favorites ---------------------------------to display favorites")
    print("--add_to_favorites  [movie name]-------------to add movie to favorites")
    print("--remove from favorites [movie name] --------to remove movie from favorites")
    print("--play [movie name] -------------------------to play movie")
    print("--download_subtitle [movie name] ------------to download subtitle")
    print("--cast [movie name]--------------------------to display movie cast")
    print("--overview [movie name]----------------------to display overview of movie")
            

if __name__=="__main__":
    system_arguments()
