import socket
import threading
import tqdm
from FileIO import File
import database as db

global files 
files=[]
directory="server_files"+r"/"
def Recieved_files(conn:socket,addy):
    
    while True:
            data = conn.recv(4096)
            if not data:
                msg="no data was recieved "
                conn.sendall(msg.encode("utf-8"))
                break


            filename=data[data.index(b'\x04')+1:data.index(b'\x00')].decode("utf-8")
            #files.append(filename)
           # print(files)
            dest_username=data[:data.index(b'\x03')].decode("utf-8")
            password=data[data.index(b'\x03')+1:data.index(b'\x04')].decode("utf-8")
            
           
            filesize = int.from_bytes(data[data.index(b'\x00')+1:data.index(b'\x01')], byteorder='big')
            filedata = data[data.index(b'\x01')+1:]
            
            file = File(dest_username,password, filename,filedata)

            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            
            progress.update(len(filedata))
                
            break
    

    db.Insert(file)
    print (file)
    print(f" upload done from {addy}")
    msg="server recieved file "
    conn.sendall(msg.encode("utf-8"))    


def Display_files(conn:socket,addy):
    user=conn.recv(4096).decode("utf-8")
    my_records=db.Retrieve_Files_by_username(user)
    s=""
    l=len(my_records)
    #print(files)
    count=0

    
    if l<1:
        s="no files available"
    else:
        for file in my_records:
            count=+1
            s=f"--->({count})."+file[2]+"\n"+s
    #print(s)        
    conn.sendall(s.encode("utf-8"))

def upload_files(conn:socket,addy):

    filename=conn.recv(4096)
    my_filename=filename[:filename.index(b'\x04')]
    #print(filename)
    filename = directory+my_filename
    with open(filename, 'rb') as f:
        filedata = f.read()
    filesize = len(filedata)

    header = my_filename.encode('utf-8') + b'\x00' + filesize.to_bytes(4, byteorder='big') + b'\x01'
    conn.sendall(header + filedata)
    #print("h")


def handle_client(conn,addy):
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



