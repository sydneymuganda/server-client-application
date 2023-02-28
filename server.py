import socket
import threading
import tqdm

def Recieved_files(data:bytes):
    filename = "myfile.txt" #data[data.index(b'\x02')+1:data.index(b'\x00')].decode('utf-8')
    filesize = int.from_bytes(data[data.index(b'\x00')+1:data.index(b'\x01')], byteorder='big')
    filedata = data[data.index(b'\x01')+1:]
    with open(filename, 'wb') as f:
        f.write(filedata)
    print("done")
def Display_files():
    print("h")
def upload_files():
    print("h")


def handle_client(conn,addy):
    print(f"[ NEW CONNECTION ] at {addy} connected")

    connected=True
    while connected:
        msg=conn.recv(4096)
        msg=msg[:msg.index(b'\x02')].decode('utf-8')
      
        if msg=="!DISCONNECT":
            connected=False
        else:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                function=data[:data.index(b'\x02')].decode('utf-8')
                if function=="send":
                    Recieved_files(data)
                elif function=="view":
                    Display_files()
                elif function=="request":         
                    upload_files()

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



