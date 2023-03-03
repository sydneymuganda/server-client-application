import sqlite3

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

    def Insert():
        conn=sqlite3.connect('Server_Database.db')
        c=conn.cursor()


        conn.commit()
        conn.close()
    def Update():

        conn=sqlite3.connect('Server_Database.db')
        c=conn.cursor()


        conn.commit()
        conn.close()

    def Retrieve_Files_by_username():
        conn=sqlite3.connect('Server_Database.db')
        c=conn.cursor()


        conn.commit()
        conn.close()