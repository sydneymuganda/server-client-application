from socket import*

def send_files(s:socket):
    #something 
    print("enter name of file you would like to send !")
    filename=str(input(""))
    action="send"
    with open(filename, 'rb') as f:
        data = f.read()
    filesize = len(data)
    header = filename.encode('utf-8') + b'\x00' + filesize.to_bytes(4, byteorder='big') + b'\x01'+action.encode("utf-8")+b'\x02'
    s.sendall(header + data)

def download_files():
     #something 
      print("h")

def view_files():
    #something 
     print("h")

def prompt():
    print("what would you like to do")
    print("(1) send files.")
    print("(2) view  files.")
    print("(3) download files.")
    print ("(4) exit")
    
    option=str(input(""))

    return option

def main():
    global port,host
    client_server=socket(socket.AF_INET,socket.SOCK_STREAM) 

    port=1969
    host="127.0.0.1"

    client_server.connect((host,port))

   

    option=prompt()

    if option=="1":
        send_files(client_server)
    elif option=="2":
        view_files()
    elif option=="3":
        download_files()
    elif option=="4":
        exit(0)
    else:
        print("invalid input")                



if __name__=="__main__":
    main()        