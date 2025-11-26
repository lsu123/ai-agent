from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

#
#print("Result for current directory:")
files_info_string = get_file_content("calculator", "main.py")
print(files_info_string)

#
#print("Result for current directory:")
files_info_string = get_file_content("calculator", "pkg/calculator.py")
print(files_info_string)

#
#print("Result for current directory:")
files_info_string = get_file_content("calculator", "/bin/cat")
print(files_info_string)

#
#print("Result for current directory:")
files_info_string = get_file_content("calculator", "pkg/does_not_exist.py")
print(files_info_string)