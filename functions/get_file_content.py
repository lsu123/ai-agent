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
                content = content[:MAX_CHARS] + "[...File {file_path} truncated at 1000 characters]"
    except Exception as e:
        return(f"Error: {e}")

    return content