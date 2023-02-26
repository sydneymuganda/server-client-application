from socket import*

def send_files():
    #something 
    print("h")
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
    client_server=socket(socket.AF_INET,socket.SOCK_STREAM) 

    port=1969
    host="127.0.0.1"

    client_server.connect((host,port))

   

    option=prompt()

    if option=="1":
        send_files()
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