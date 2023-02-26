from socket import*
def main():
    server_socket=socket(socket.AF_INET,socket.SOCK_STREAM)
    port=1969
    host="127.0.0.1"
    server_socket.bind((host,port))
    server_socket.listen(5)
    files=[]
    count=0
    while True:
        clientSocket, address=server_socket.accept()
        print(f"connection established from adress {address}")


if __name__=="__main__":
    main()



