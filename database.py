import sqlite3
from FileIO import File

def Create():
    conn=sqlite3.connect('Server_Database.db')
    c=conn.cursor()

    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Server_Files' ''')

    #if the count is 1, then table exists
    if c.fetchone()[0]==1 : {
	    print('SERVER DATABASE PREPARED FOR USE')
    }
    else : {    
        c.execute("""CREATE TABLE Server_Files(
         username text,
         password text,
         file text,
         data BLOB


        )""") }
   
    conn.commit()
    conn.close()

def Insert(f:File):
    conn=sqlite3.connect('Server_Database.db')
    c=conn.cursor()
        
    c.execute( "INSERT INTO Server_Files VALUES (:username, :password, :file, :data)",
                {'username':f.username,
                    'password':f.password,
                    'file':f.filename,
                    'data':f.data}
    )

    conn.commit()
    conn.close()
        
def Update(f,l):

    conn=sqlite3.connect('Server_Database.db')
    c=conn.cursor()


    conn.commit()
    conn.close()

def Retrieve_Files_by_username():
    conn=sqlite3.connect('Server_Database.db')
    c=conn.cursor()


    conn.commit()
    conn.close()