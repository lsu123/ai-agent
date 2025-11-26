from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    import os

    target_directory = os.path.join(working_directory, directory)
    files_info = []
    files_info_string = ""

    if not os.path.abspath(target_directory).startswith(os.path.abspath(working_directory)):
        return ValueError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

    if not os.path.isdir(target_directory):
        return ValueError(f'Error: "{directory}" is not a directory') 

    try:
        #for root, _, files in os.walk(target_directory):
        for file in os.listdir(target_directory):
            #for file in files:
            #file_path = os.path.join(root, file)
            file_path = os.path.join(target_directory, file)
            #print(file_path) 
            #file_path = file.path
            #relative_path = os.path.relpath(file, working_directory)
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            files_info.append({
                " - ": file,
                " file_size=": size,
                ", is_dir=": is_dir
            })  
            files_info_string += f" - {file}: file_size={size}, is_dir={is_dir}\n"  
    except Exception as e:
        return(f"Error accessing files: {e}")

    return files_info_string