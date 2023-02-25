import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

port=6060
host="127.0.0.1"

s.connect((host,6060))

filename="testfile.txt"

with open(filename, 'rb') as f:
    data = f.read()
filesize = len(data)
header = filename.encode('utf-8') + b'\x00' + filesize.to_bytes(4, byteorder='big') + b'\x01'
s.sendall(header + data)

s.close()