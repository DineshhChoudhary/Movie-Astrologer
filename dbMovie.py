import sqlite3

class MovieDatabase:
    def __init__(self):
        self.con=sqlite3.connect('MovieDatabase.db')
        self.c=self.con.cursor()

    def dbcommit(self):
        self.con.commit()

    def dbExecuteQuery(self,query):
        result=self.c.execute(query)
        return result
    '''def dbexecuteMany(self,query,listData):
        result=self.c.executemany(query,listData)
        return result'''
    def dbinsertMovieDetails(self,listData):
        self.c.execute("insert into moviedetails values(?,?,?,?,?,?,?,?,?)",(listData[0],listData[1],listData[2],listData[3],listData[4],listData[5],listData[6],listData[7],listData[8]))
    def dbinsertToWatched(self,listData):
        self.c.execute("insert into watched values(?,?,?)",(listData[0],listData[1],"true"))
    def dbremoveFromWatched(self,query):
        self.c.execute("delete from watched where title='%s'" %query)

    def dbinsertToFavorites(self,listData):
        self.c.execute("insert into favorites values(?,?,?)",(listData[0],listData[1],"true"))
    def dbremoveFromFavorites(self,query):
        self.c.execute("delete from favorites where title='%s'" %query)
    def dbAddPath(self,data):
        result=self.c.execute("select * from path where moviepath='%s'" %data)
        for r in result:
            return True
        self.c.execute("insert into path values(?)",(data,))
    def dbRemovePath(self,query):
        self.c.execute("delete from path where moviepath='%s'" %query)
        
    
    def dbinsertMovieGenre(self,movieid,listData):
        for genreid in listData:
            self.c.execute("insert into moviegenre values(?,?)",(movieid,genreid))
    def dbinsertGenreDetails(self,listdic):
        for genre in listdic['genres']:
            flag=0
            result=self.c.execute("select genreid from genredetails where genreid=%s" %genre['id'])
            for r in result:
                if r==genre['id']:
                    flag=1
            if flag==0:
                self.c.execute("insert into genredetails values(?,?)",(genre['id'],genre['name']))
    def dbgetMovieLocation(self,moviename):
        result=self.c.execute("select movielocation,movieextension from playmoviepath where moviename='%s'" %moviename)
        for r in result:
            return r
    def dbsetMovieLocation(self,moviename,movielocation,movieext):
        self.c.execute("insert into playmoviepath values(?,?,?)",(moviename,movielocation,movieext))

    def dbsetMovieCast(self,movieid,moviecast):
        for cast in moviecast['cast']:
            if cast['order']>8:
                break
            self.c.execute("insert into moviecast values(?,?,?)",(movieid,cast['character'],cast['name']))

    def dbgetMovieCast(self,movieid):
        result=self.c.execute("select castname,castcharacter from moviecast where movieid=%s" %movieid)
        return result
        
    def dbCloseConnection(self):
        self.con.close()

    def isPresent(self,query):
        result=self.c.execute("select title from moviedetails where id=%s" %query)
        for r in result:
            return True
        return False
    
    
    def dbcreate(self):
        try:
            self.c.executescript("""
                create table moviecast(
                movieid,
                castcharacter,
                castname
                );
                create table playmoviepath(
                moviename,
                movielocation,
                movieextension
                );
                create table favorites(
                id,
                title,
                watch_status
                );
                create table watched(
                id,
                title,
                watch_status
                );
                create table path(
                moviepath
                );
                create table moviedetails(
                id,
                imdbrating,
                title,
                language,
                adult,
                overview,
                poster_path,
                backdrop_path,
                release_date
                );

                create table moviegenre(
                id,
                genreid
                );

                create table genredetails(
                genreid,
                genrename
                );
                
                """)
        except:
            return
