from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file in the specified directory as a subprocess, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to write to, relative to the working directory. If not provided or file not found, returns an error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If not provided or file not found, returns an error.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    import os

    # Construct the full path to the file
    full_path = os.path.join(working_directory, file_path)

    #if not os.path.abspath(target_directory).startswith(os.path.abspath(working_directory)):
    #    return ValueError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write the content to the file
        with open(full_path, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)\n{content}'
    except Exception as e:
        return f"Error writing file: {e}"
