import os, subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    
    abs_working_directory = os.path.abspath(working_directory)
    abs_path = os.path.abspath(full_path)

    if not abs_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            args=["python", abs_path] + args,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory,
        )

        final_string = ""
        if completed_process.stdout:
            final_string += "STDOUT:\n" + completed_process.stdout + "\n"
        if completed_process.stderr:
            final_string += "STDERR:\n" + completed_process.stderr + "\n"
        if completed_process.returncode != 0:
            final_string += f"Process exited with code {completed_process.returncode}\n"
        
        if not final_string:
            return "No output produced"
        else:
            return final_string.strip()
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    