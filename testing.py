import database as  db  
import math
#print(db.Retrieve_Files_by_filename("1234","fruits.txt"))


def work_on_sections(my_data, section_size):
    size = len(my_data)
    num_sections = math.ceil((size + section_size - 1) // section_size ) # Round up division
    start_index = 0
    for section in range(num_sections):
        end_index = min(start_index + section_size, size)
        section_data = my_data[start_index:end_index]
        print(section_data)
        start_index = end_index  

def main():
     
     filename="movies.txt"
     with open(filename, 'rb') as f:
          data=f.read()

     for i in range (0,len(data),1024):
          print (data[i:i+4])
     
     print("test")
     work_on_sections(data,4)
     print("test2")
     work_on_sections(data,1024)


if __name__=="__main__" :
     main()  