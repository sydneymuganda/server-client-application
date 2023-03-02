import socket
import tqdm

def send_files(s:socket):
    #something 
    print("enter name of file you would like to send !")
    filename=str(input(""))
    action="send"
    header =action.encode("utf-8")+b'\x02'
    s.sendall(header)
    with open(filename, 'rb') as f:
        data = f.read()
    filesize = len(data)
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    header = filename.encode('utf-8') + b'\x00' + filesize.to_bytes(4, byteorder='big') + b'\x01'
    s.sendall(header + data)
    progress.update(filesize)
    print("sent")

def download_files():
     #something 
      print("h")

def view_files():
    #something 
     print("h")

def breakConnection(client_server:socket):
    action="!DISCONNECT"
    #client_server.send("!DISCONNECT".encode("utf-8"))
    header =action.encode("utf-8")+b'\x02'
    
    client_server.sendall(header)


def prompt():
    print("what would you like to do?")
    print("(1) send files.")
    print("(2) view  files.")
    print("(3) download files.")
    print ("(4) exit")
    
    

def main():
    global port,host
    client_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    port=1969
    host="127.0.0.1"

    client_server.connect((host,port))

    prompt()
    option="0"

    while option!="4":
        option=str(input(""))

        if option=="1":
            send_files(client_server)
        elif option=="2":
             view_files()
        elif option=="3":
            download_files()
        elif option=="4":
            breakConnection(client_server)
            break
        else:
            print("invalid input")                
        
        prompt()
        

    client_server.close()     


if __name__=="__main__":
    main()        