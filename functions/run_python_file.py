def run_python_file(working_directory, file_path, args=[]):
    import os
    import subprocess
    import sys

    # Construct the full path to the Python file
    full_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'

    if os.path.splitext(full_path)[1] != '.py':
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Run the Python file as a subprocess with a 30 second timeout
        result = subprocess.run(
            [sys.executable, full_path] + args,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30,
        )

        if result.stdout is None:
            return f"No output produced."

        if result.returncode != 0:
            return f"STDOUT:{result.stdout} STDERR:{result.stderr} Process exited with code {result.returncode}"
        else:
            return f"STDOUT:{result.stdout} STDERR:{result.stderr}"

    except subprocess.TimeoutExpired as e:
        # Process did not finish within timeout; include any partial output if available
        out = getattr(e, 'stdout', None)
        err = getattr(e, 'stderr', None)
        msg = f"Error: Process timed out after {e.timeout} seconds."
        if err:
            msg += f" Stderr: {err}"
        if out:
            msg += f" Stdout (partial): {out}"
        #return msg
        return f"Error: executing Python file: {e}"
    except Exception as e:
        return f"Error: executing Python file: {e}"