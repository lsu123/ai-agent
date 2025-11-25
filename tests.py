from functions.get_files_info import get_files_info

#
print("Result for current directory:")
files_info_string = get_files_info("calculator", ".")
print(files_info_string)

#
print("Result for 'pkg' directory:")
files_info_string = get_files_info("calculator", "pkg")
print(files_info_string)

#
print("Result for '/bin' directory:")
files_info_string = get_files_info("calculator", "/bin")
print(files_info_string)

#
print("Result for '../' directory:")
files_info_string = get_files_info("calculator", "../")
print(files_info_string)