import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=6060
host="127.0.0.1"
s.bind((host,port))
s.listen(5)
files=[]
count=0
while True:
    clientSocket, address=s.accept()
    print(f"connection established from adress {address}")
    count+=1
    while True:
            data = clientSocket.recv(4096)
            if not data:
                break
            filename = "newfile.txt"
            filesize = int.from_bytes(data[data.index(b'\x00')+1:data.index(b'\x01')], byteorder='big')
            filedata = data[data.index(b'\x01')+1:]
            with open(filename, 'wb') as f:
                f.write(filedata)
    print(count) 
    if count>1:
         break           