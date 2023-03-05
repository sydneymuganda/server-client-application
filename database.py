"""
This script creates the database to allow file data to be saved onto a database
and specifies functions to be used

Author: Sydney Muganda (mgnsyd001@myuct.ac.za)
Date: 20th february 2023
"""

import sqlite3
from FileIO import File

def Create():
    """
    Creates a SQLite database for storing file data, if it does not already exist.

    Returns:
        None
    """
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
    """
    Inserts a file into the Server_Files table in the database, or updates the data
    for an existing file if it has the same username, password, and file name.

    Args:
        f (File): The File object to be inserted.

    Returns:
        None
    """
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
        
            
    if count>=1:
        pass
    else:
        c.execute( "INSERT INTO Server_Files VALUES (:username, :password, :file, :data)",
                    {'username':f.username,
                        'password':f.password,
                        'file':f.filename,
                        'data':f.data}
        )
       
    conn.commit()
    conn.close()
        
def Update(f:File):
    """
    Updates the Server_Files table in the database with the new data for a file.

    Args:
        f (File): The File object with the updated data.
        

    Returns:
        None
    """

    conn=sqlite3.connect('Server_Database.db')
    c=conn.cursor()


    conn.commit()
    conn.close()

def Retrieve_Files_by_username(username):
    """
    Retrieves all files from the Server_Files table in the database 
    with the given username.

    Args:
        username (str): The username associated with the files to retrieve.

    Returns:
        list: A list of tuples representing the retrieved files.
    """
    conn=sqlite3.connect('Server_Database.db')
    c=conn.cursor()
    
    c.execute("SELECT * FROM Server_Files WHERE username=:username OR username='everyone' ",{'username':username})
    records=c.fetchall()
    conn.commit()
    conn.close()
    return records

def Retrieve_Files_by_filename(username,filename):
    """
    Retrieves all files from the Server_Files table in the database 
    with the given username and filename

    Args:
        username (str): The username associated with the files to retrieve.
        filename (str): The flename associated with the files to retrieve

    Returns:
        list: A list of tuples representing the retrieved files.
    """
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