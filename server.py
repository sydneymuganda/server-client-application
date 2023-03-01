import socket
import threading
import tqdm

def Recieved_files(conn:socket,addy):
    
    while True:
            data = conn.recv(4096)
            if not data:
                break
            filename = "myfile.txt"
            filesize = int.from_bytes(data[data.index(b'\x00')+1:data.index(b'\x01')], byteorder='big')
            filedata = data[data.index(b'\x01')+1:]
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, 'wb') as f:
                f.write(filedata)
                progress.update(len(filedata))
                
            break

    print(f" upload done from {addy}")    


def Display_files():
    print("h")
def upload_files():
    print("h")


def handle_client(conn,addy):
    print(f"[ NEW CONNECTION ] at {addy} connected")
    
    msg=conn.recv(4096)
        
   
    msg=msg[:msg.index(b'\x02')].decode('utf-8')
    
    connected=True
    while connected:
       
      
        if msg=="!DISCONNECT":
            connected=False
        elif msg=="send":
            Recieved_files(conn,addy)
            
            msg=conn.recv(4096)
            
            
        elif msg=="view":
            Display_files()
            msg=conn.recv(4096)
        elif msg=="request":         
            upload_files()
            msg=conn.recv(4096)

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
    files=[]
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



