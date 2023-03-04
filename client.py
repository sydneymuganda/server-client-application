import socket
import tqdm

def password_prompt():
    print("would you like this file to be ","(a)protected","(b)unprotected",sep="\n")
    access=str(input(""))
    return access

def send_files(s:socket):
    #something 
    print("enter name of file you would like to send !")
    filename=str(input(""))
    access=password_prompt()
   
    while True:
        if access.lower()=="a":
            
            print("enter name of user you would like to send to !")

            dest_user=str(input(""))

            print("enter access password of file you are sending !")
            password=str(input(""))
            break
        elif access.lower()=="b":
            
            dest_user="everyone"
            password="none"
            break
        else:
            print("invalid input please enter either a or b ")
            access=password_prompt()   
    
    action="send"
    header =action.encode("utf-8")+b'\x02'
    s.sendall(header)
    with open(filename, 'rb') as f:
        data = f.read()
    filesize = len(data)
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    header = dest_user.encode("utf-8")+b'\x03'+password.encode("utf-8")+b'\x04'+ filename.encode('utf-8') + b'\x00' + filesize.to_bytes(4, byteorder='big') + b'\x01'
    s.sendall(header + data)
    progress.update(filesize)
   
    print()
    print(s.recv(4096).decode("utf-8"))

def download_files(s:socket):
     #something 

     print("enter name of file you would like to download !")
     filename=str(input(""))
     action="request" 
     header =action.encode("utf-8")+b'\x02' 
     s.sendall(header)
     header=filename.encode("utf-8")+b'\x04' 
     s.sendall(header)
     
     data = b''
     while True:
        recv = s.recv(4096)
        if not recv:
            break
        data += recv
        break
     

     filename =data[:data.index(b'\x00')].decode("utf-8")
     filesize = int.from_bytes(data[data.index(b'\x00')+1:data.index(b'\x01')], byteorder='big')
     filedata = data[data.index(b'\x01')+1:]

     with open(filename, 'wb') as f:
        f.write(filedata)

     #print("h")

def view_files(s:socket):
     

    action="view"
    header =action.encode("utf-8")+b'\x02'
    s.sendall(header)

    s.sendall(username.encode("utf-8"))
    

    
    message=s.recv(4096)
    
    print("----AVAILABLE FILES----")
    print(message.decode("utf-8"))
    

def breakConnection(client_server:socket):
    action="!DISCONNECT"
    
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
    global username
    username=str(input("please enter your username:\n"))
    prompt()
    option="0"

    while option!="4":
        option=str(input(""))

        if option=="1":
            send_files(client_server)
        elif option=="2":
             view_files(client_server)
        elif option=="3":
            download_files(client_server)
        elif option=="4":
            breakConnection(client_server)
            break
        else:
            print("invalid input")                
        
        prompt()
        

    client_server.close()     


if __name__=="__main__":
    main()        