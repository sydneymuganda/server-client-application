"""
This script creates the application 
to allow a client to send,recieve and view files to and from a server

Author: Sydney Muganda (mgnsyd001@myuct.ac.za)
Date: 20th february 2023
"""
import socket
import tqdm
#TODO :fix file transfer for large data


def password_prompt():
    ''''
    This function prompts the user to specify whether a given file should be protected or not! for flexibility

    :return: the reultant option whether a or b
    '''
    print("would you like this file to be ","(a)protected","(b)unprotected",sep="\n")
    access=str(input(""))
    return access

def send_files(s:socket):
    ''''
    This function prompts the client to send a file to the server!

    :param s: socket used to connect to the server
    :return: nothing

    '''
    
    print("enter name of file you would like to send !")
    filename=str(input("")) #prompting user to enter filename
    access=password_prompt() # prompting user to specify whether the file will be proctected or unprotected
   
    while True:# while loop to loop until correct acces input is put in (a) or (b)
        if access.lower()=="a":
            
            print("enter name of user you would like to send to !")

            dest_user=str(input("")) #if proctected then enter target user and pasword

            print("enter access password of file you are sending !")
            password=str(input(""))
            break
        elif access.lower()=="b":
            #if unprotected no password and target users are everyone
            dest_user="everyone"
            password="none"
            break
        else: 
            print("invalid input please enter either a or b ")
            access=password_prompt()   
    
    action="send"
    header =action.encode("utf-8")+b'\x02'
    s.sendall(header) #sends information to the server to prepare to recieve files
    with open(filename, 'rb') as f: #open given filename and reads the data as bytes
        data = f.read()

    filesize = len(data)
    #TODO:check if tqm dictionary is in the standard library or specify its need in the report
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024) #progress bar to show progress of file download
   
   #header which is compromised of (target user),(password),(filename),(filesize),(data)
    header = dest_user.encode("utf-8")+b'\x03'+password.encode("utf-8")+b'\x04'+ filename.encode('utf-8') + b'\x00' + filesize.to_bytes(4, byteorder='big') + b'\x01'
    s.sendall(header + data) #sends to server
    progress.update(filesize)
   
    print()
    print(s.recv(4096).decode("utf-8")) #prints affirmation of completion fropm server

def download_files(s:socket):
     ''''
    This function prompts the client to download a file from the server!

    :param s: socket used to connect to the server
    :return: nothing

    ''' 
     
     print("enter name of file you would like to download !")
     filename=str(input("")) #prompt user to request the file they would like to download
     action="request" 
     header =action.encode("utf-8")+b'\x02' 
     s.sendall(header) #send a request message to server
     header=filename.encode("utf-8")+b'\x04'+username.encode("utf-8") 
     s.sendall(header) #sends a header which contains the filename and username of client
     

     reply_message=s.recv(4096).decode("utf-8")
     # waits to for feedback on available files and their status ie :protected or not
     
     
     print(reply_message) 
     if reply_message=="no files available":
        
         
         return
     
     option=str(input("Enter file you would like to download:\n")) #enter option of file you would like to download
     s.sendall(option.encode("utf-8")) #send the reply of what you requested


     feedback=s.recv(4096).decode("utf-8") #recives feedback from server whether requested file requires a password

     if feedback=="ok":
         s.sendall("ok".encode("utf-8")) #if not send back ok

     else:
         print(feedback) 
         reply=str(input(""))
         s.sendall(reply.encode("utf-8"))  #if yes send back the password

     acess_control=s.recv(4096).decode("utf-8") #waits for server to send back an ok for valid password 

     if acess_control!="ok": #if invalid will print invalid and end the program
         print(acess_control)
         prompt()
         return     
     
     data = b''
     while True:#while loop to recieve the data as a header
        recv = s.recv(4096)
        if not recv:
            break
        data += recv
        break
     
        
     

     filename =data[:data.index(b'\x00')].decode("utf-8") #takes in the recieved filename
     filesize = int.from_bytes(data[data.index(b'\x00')+1:data.index(b'\x01')], byteorder='big') #takes in recieved filesize
     filedata = data[data.index(b'\x01')+1:] #takes in file data
     directory="downloaded_files"+r'/'+filename #location of saved files
     progress = tqdm.tqdm(range(len(filedata)), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
     progress.update() #progress bar to show the the progress of download

     with open(directory, 'wb') as f: #write the file to the directory
        f.write(filedata)

     print("succesfully downladed")# print succesfully downloaded

def view_files(s:socket):
    """
       
     Sends a request to the server to view the available files
     according to client username  then displays them on the client console.

        Args:
            s: socket object that represents the client-server connection.

        Returns:
            None
    
    """

    action="view"
    header =action.encode("utf-8")+b'\x02'
    s.sendall(header) #sends the action header

    s.sendall(username.encode("utf-8")) #sends the username
    

    
    message=s.recv(4096)
    
    print("----AVAILABLE FILES----")
    print(message.decode("utf-8"))#prints available files
    

def breakConnection(client_server:socket):
    """
    Sends a disconnection request to the server
      and closes the client-server connection.

    Args:
        client_server: socket object that represents the client-server connection.

    Returns:
        None
    """

    action="!DISCONNECT"
    
    header =action.encode("utf-8")+b'\x02'
    
    client_server.sendall(header)


def prompt():
    """
    prints out a message prompt for possible user input


    Returns:
        None
    
    """
    print("what would you like to do?")
    print("(1) send files.")
    print("(2) view  files.")
    print("(3) download files.")
    print ("(4) exit")
    
    

def main():
    """
    Main function that handles user input and performs actions based on that input.

    Returns:
        None
    """
    global port,host
    client_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    port=1969
    host="127.0.0.1"

    client_server.connect((host,port)) #establishes connection
    global username
    username=str(input("please enter your username:\n")) #the clients username
    prompt()
    option="0"

    while option!="4":#loops until client disconnects
        option=str(input(""))

        if option=="1":
            send_files(client_server)
        elif option=="2":
             view_files(client_server)
        elif option=="3":
            download_files(client_server)
        elif option=="4":
            breakConnection(client_server)
            break
        else:
            print("invalid input")                
        
        prompt()
        

    client_server.close()     #closes connection


if __name__=="__main__":
    main()        