import os
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
    full_path = os.path.join(working_directory, directory)
    
    abs_working_directory = os.path.abspath(working_directory)
    abs_path = os.path.abspath(full_path)
    
    
    if not abs_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        file_list = os.listdir(abs_path)
    except Exception as e:
        return f"Error: {e}"
    
    new_list = []
    for name in file_list:
        new_path = os.path.join(abs_path, name)
        
        try:
            size = os.path.getsize(new_path)
            is_dir = os.path.isdir(new_path)
        except Exception as e:
            return f"Error: {e}"
        
        new_list.append(f'- {name}: file_size={size} bytes, is_dir={is_dir}')
    return "\n".join(new_list)

