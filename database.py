"""
This script creates the database to allow file data to be saved onto a database
and specifies functions to be used

Author: Sydney Muganda (mgnsyd001@myuct.ac.za)
Date: 20th february 2023
"""

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
    
    count=0
    c.execute("SELECT * FROM Server_Files WHERE username=:username AND password=:password AND file=:file ",{'username':f.username, 'password':f.password,'file':f.filename})
    records=c.fetchall()
        
    for i in records:
        if ((f.filename in i) and (f.username in i) and (f.password in i)):
            count+=1
            c.execute( """UPDATE Server_Files SET data= :data WHERE username=:username AND password=:password AND file=:file """,
                      {'username':f.username, 
                       'password':f.password,
                       'file':f.filename,
                       'data':f.data} )
           # print("updated")
            
    if count>=1:
        pass
    else:
        c.execute( "INSERT INTO Server_Files VALUES (:username, :password, :file, :data)",
                    {'username':f.username,
                        'password':f.password,
                        'file':f.filename,
                        'data':f.data}
        )
        #print("inserted")
    conn.commit()
    conn.close()
        
def Update(f,l):

    conn=sqlite3.connect('Server_Database.db')
    c=conn.cursor()


    conn.commit()
    conn.close()

def Retrieve_Files_by_username(username):
    conn=sqlite3.connect('Server_Database.db')
    c=conn.cursor()
    
    c.execute("SELECT * FROM Server_Files WHERE username=:username OR username='everyone' ",{'username':username})
    records=c.fetchall()
    conn.commit()
    conn.close()
    return records

def Retrieve_Files_by_filename(username,filename):
    conn=sqlite3.connect('Server_Database.db')
    c=conn.cursor()
    
    c.execute("SELECT * FROM Server_Files WHERE (username=:username AND file=:file) OR (username='everyone' AND file=:file2) ",
              {
                        'username':username,
                        
                        'file':filename,
                        
                        'file2':filename,
              })
    records=c.fetchall()
    conn.commit()
    conn.close()
    return records