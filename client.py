"""
This script creates the application 
to allow a client to send,recieve and view files to and from a server

Author: Sydney Muganda (mgnsyd001@myuct.ac.za)
Date: 20th february 2023
"""
import socket
import tqdm

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
     filename=str(input(""))
     action="request" 
     header =action.encode("utf-8")+b'\x02' 
     s.sendall(header)
     header=filename.encode("utf-8")+b'\x04'+username.encode("utf-8") 
     s.sendall(header)
     


     print(s.recv(4096).decode("utf-8"))

     option=str(input("Enter file you would like to download:\n"))
     s.sendall(option.encode("utf-8"))

     feedback=s.recv(4096).decode("utf-8")

     if feedback=="ok":
         s.sendall("ok".encode("utf-8"))

     else:
         print(feedback.encode("utf-8")) 
         reply=str(input(""))
         s.sendall(reply.encode("utf-8"))  

     acess_control=s.recv(4096).decode("utf-8")    

     if acess_control!="ok":
         print(acess_control)
         return     
     
     data = b''
     while True:
        recv = s.recv(4096)
        if not recv:
            break
        data += recv
        break
     
        
     

     filename =data[:data.index(b'\x00')].decode("utf-8")
     filesize = int.from_bytes(data[data.index(b'\x00')+1:data.index(b'\x01')], byteorder='big')
     filedata = data[data.index(b'\x01')+1:]
     directory="downloaded_files"+r'/'+filename
     progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
     progress.update()

     with open(directory, 'wb') as f:
        f.write(filedata)

     print("succesfully downladed")

def view_files(s:socket):
     

    action="view"
    header =action.encode("utf-8")+b'\x02'
    s.sendall(header)

    s.sendall(username.encode("utf-8"))
    

    
    message=s.recv(4096)
    
    print("----AVAILABLE FILES----")
    print(message.decode("utf-8"))
    

def breakConnection(client_server:socket):
    action="!DISCONNECT"
    
    header =action.encode("utf-8")+b'\x02'
    
    client_server.sendall(header)


def prompt():
    print("what would you like to do?")
    print("(1) send files.")
    print("(2) view  files.")
    print("(3) download files.")
    print ("(4) exit")
    
    

def main():
    global port,host
    client_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    port=1969
    host="127.0.0.1"

    client_server.connect((host,port))
    global username
    username=str(input("please enter your username:\n"))
    prompt()
    option="0"

    while option!="4":
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
        

    client_server.close()     


if __name__=="__main__":
    main()        