from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to read, relative to the working directory. If not provided or file not found, returns an error.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    import os
    from config import MAX_CHARS

    target_file_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(target_file_path).startswith(os.path.abspath(working_directory)):
        return ValueError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

    if not os.path.isfile(target_file_path):
        return ValueError(f'Error: File not found or is not a regular file: "{file_path}"') 

    try:
        with open(target_file_path, 'r') as file:
            content = file.read()
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS] + f'"[...File "{file_path}" truncated at 1000 characters]"'
    except Exception as e:
        return(f"Error: {e}")

    return content