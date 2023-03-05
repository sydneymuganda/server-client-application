class File:
    """
     
     A class representing a file.

     Attributes:
        username (str): The username associated with the file.
        password (str): The password associated with the file.
        filename (str): The name of the file.
        data (bytes): The data contained in the file.
   
    
    
    """

    def __init__(self,username,password,filename,data) :
         """
         
        Constructs a new File object with the given parameters.

        Args:
            username (str): The username associated with the file.
            password (str): The password associated with the file.
            filename (str): The name of the file.
            data (bytes): The data contained in the file.
     
         """
         self.username=username
         self.password=password
         self.filename=filename
       
         self.data=data


    def __repr__(self) :
         """"
         
         
         Returns a string representation of the File object.

         Returns:
             str: A string representation of the File object.
        
         
         """
         return "File ('{}','{}','{}')".format(self.username,self.password,self.filename,)
              