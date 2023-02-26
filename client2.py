import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

port=8000
host="127.0.0.1"

s.connect((host,port))

data = b''
while True:
    recv = s.recv(4096)
    if not recv:
        break
    data += recv

filename ="file2.txt"
filesize = int.from_bytes(data[data.index(b'\x00')+1:data.index(b'\x01')], byteorder='big')
filedata = data[data.index(b'\x01')+1:]

with open(filename, 'wb') as f:
    f.write(filedata)

s.close()