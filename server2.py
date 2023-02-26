import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=8000
host="127.0.0.1"
s.bind((host,port))
s.listen(5)
files=[]
count=0

filename = 'testfile.txt'
with open(filename, 'rb') as f:
    filedata = f.read()
filesize = len(filedata)
header = filename.encode('utf-8') + b'\x00' + filesize.to_bytes(4, byteorder='big') + b'\x01'

while True:
    conn, address = s.accept()
    with conn:
        print(f"connection established from adress {address}")
   
        conn.sendall(header + filedata)