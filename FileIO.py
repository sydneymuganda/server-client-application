class File:
   

    def __init__(self,username,password,filename,data) :
         self.username=username
         self.password=password
         self.filename=filename
       
         self.data=data


    def __repr__(self) :
         return "File ('{}','{}','{}','{}')".format(self.username,self.password,self.filename,)
              