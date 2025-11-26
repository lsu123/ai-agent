from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

files_info_string = run_python_file("calculator", "main.py")
print(files_info_string)

files_info_string = run_python_file("calculator", "main.py", ["3 + 5"])
print(files_info_string)

files_info_string = run_python_file("calculator", "tests.py")
print(files_info_string)

files_info_string = run_python_file("calculator", "../main.py")
print(files_info_string)

files_info_string = run_python_file("calculator", "nonexistent.py")
print(files_info_string)

files_info_string = run_python_file("calculator", "lorem.txt")
print(files_info_string)


#files_info_string = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
#print(files_info_string)

#
#print("Result for current directory:")
#files_info_string = get_file_content("calculator", "main.py")
#print(files_info_string)
