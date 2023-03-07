"""
This script creates the application 
to allow a server to send and recieve  to and from a client

Author: Sydney Muganda (mgnsyd001@myuct.ac.za)
Date: 20th february 2023
"""

import math
import socket
import threading
import tqdm
from FileIO import File
import database as db

packet_size=1024

def Recieved_files(conn:socket,addy):
    """
    This function receives files from the client, and saves them in the database.

    :param conn: A socket object that represents a client-server connection.
    :param addy: A tuple containing the IP address and port number of the client.
    """
    data_details=conn.recv(4096)
    filedata=b''
    filesize = int.from_bytes(data_details[data_details.index(b'\x00')+1:data_details.index(b'\x01')], byteorder='big')
    filename=data_details[data_details.index(b'\x04')+1:data_details.index(b'\x00')].decode("utf-8")
    
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    
    empty_file=False
    count=0
    while True:
            data = conn.recv(packet_size)
            if  data==b"end"or data==b"" or filesize==len(filedata):
               
                if count==0: empty_file=True
                break


           
            filedata = filedata+data
            
            #print(filedata)

            
            
            progress.update(len(filedata))
            count=count+1
            
            
                
            
    

    if empty_file:
         msg="no file recieved "
         conn.sendall(msg.encode("utf-8")) 

    else:        
        dest_username=data_details[:data_details.index(b'\x03')].decode("utf-8")
        password=data_details[data_details.index(b'\x03')+1:data_details.index(b'\x04')].decode("utf-8")
                
            
            
        file = File(dest_username,password, filename,filedata)
        db.Insert(file)
        print(f" upload done from {addy}")
        msg="server recieved file "
        conn.sendall(msg.encode("utf-8")) 

def Display_files(conn:socket,addy):
    """
    This function displays the files stored in the database for a given user.

    :param conn: A socket object that represents a client-server connection.
    :param addy: A tuple containing the IP address and port number of the client.

    """

    user=conn.recv(4096).decode("utf-8")
    my_records=db.Retrieve_Files_by_username(user)
    s=""
    l=len(my_records)
    
    count=0

    
    if l<1:
        s="no files available"
    else:
        for file in my_records:
            count+=1
            s=s+f"--->({count})"+file[2]+"\n"
         
    conn.sendall(s.encode("utf-8"))

def upload_files(conn:socket,addy):
    """
    This function allows the client to download a file from the server.

    :param conn: A socket object that represents a client-server connection.
    :param addy: A tuple containing the IP address and port number of the client.

    """


    
    filename=conn.recv(4096)
    
    
    my_filename=filename[:filename.index(b'\x04')].decode("utf-8")
    user=filename[filename.index(b'\x04')+1:].decode("utf-8")
    
    # print(user,my_filename)
    
    my_records=db.Retrieve_Files_by_filename(user,my_filename)
    #print(my_records)
    l=len(my_records)
    count=(0)
    s=""
    if l<1:
        s="no files available"
        conn.sendall(s.encode("utf-8"))
        
        return
    else:
        prompt="choose the number of the file you would like to download!\n"
        for file in my_records:
            count+=1
            s=s+f"--->({count})"+file[2]+"\n"
        s=prompt+s    

    conn.sendall(s.encode("utf-8"))    
    
    chosen_file=int(conn.recv(4096).decode("utf-8"))-1

    if my_records[chosen_file][1]=="none":
        conn.sendall("ok".encode("utf-8")) 
        conn.recv(4096)
        filedata=my_records[chosen_file][3]
        conn.sendall("ok".encode("utf-8"))
    else:
        conn.sendall("Enter password".encode("utf-8"))  
        password=  conn.recv(4096).decode("utf-8")  
        if password==my_records[chosen_file][1]:
            filedata=my_records[chosen_file][3]
            conn.sendall("ok".encode("utf-8"))
        else:
            conn.sendall("invalid".encode("utf-8"))
            return      
   
        
    filesize = len(filedata)

    header = my_filename.encode('utf-8') + b'\x00' + filesize.to_bytes(4, byteorder='big') + b'\x01'
    conn.sendall(header ) #only sending header

    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    work_on_sections(conn,filedata,packet_size,progress)        
    
    print()
    print(f" download done from {addy}")
    msg="server sent file "
    conn.sendall(msg.encode("utf-8"))    
def work_on_sections(s:socket,my_data, section_size,progress):
    ''''
    divides the data to be sent in sections

    :param s: socket used to connect to the server
    :param my_data: data in bytes to be sent
    :param secction_size:byte buffer size
    :param progress: progress bar
    :return: nothing

    ''' 
    size = len(my_data)
    num_sections = math.ceil((size + section_size - 1) // section_size ) # Round up division
    start_index = 0
    for section in range(num_sections):
        end_index = min(start_index + section_size, size)
        section_data = my_data[start_index:end_index]
        s.sendall(section_data)
        start_index = end_index  
        progress.update(len(section))
def handle_client(conn,addy):
    """
    This function handles multithreded client-server connection by receiving client requests 
    and invoking the appropriate function.
    in so doing allows multiple client connections

    :param conn: A socket object that represents a client-server connection.
    :param addy: A tuple containing the IP address and port number of the client.
    
    """

    print(f"[ NEW CONNECTION ] at {addy} connected")
    
    msg=conn.recv(4096)
        
   
    msg=msg[:msg.index(b'\x02')].decode('utf-8')
    
    connected=True
    while connected:
       
      
        if msg=="!DISCONNECT":
            break
            
        elif msg=="send":
            Recieved_files(conn,addy)
            
            msg=conn.recv(4096)
            msg=msg[:msg.index(b'\x02')].decode('utf-8')
            
        elif msg=="view":
            Display_files(conn,addy)
            msg=conn.recv(4096)
            msg=msg[:msg.index(b'\x02')].decode('utf-8')

        elif msg=="request":   
             
            upload_files(conn,addy)
            msg=conn.recv(4096)
            msg=msg[:msg.index(b'\x02')].decode('utf-8')

        else: break    
            

    print(f"{addy} DISCONNECTED")
    conn.close()        

def main():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    global port,host
    port=1969
   
    host="127.0.0.1"
    server_socket.bind((host,port))
    server_socket.listen(5)
    db.Create()
    count=0
    while True:
        clientConn, address=server_socket.accept()
        thread=threading.Thread(target=handle_client,
                                args=(clientConn,address))
        thread.start()
        count=threading.active_count()-1
        print("connection established with",count,"active connections")


        


if __name__=="__main__":
    main()



