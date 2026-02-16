import os

def get_files_info(working_directory, directory="."):

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir])
        if valid_target_dir != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        contents = os.listdir(target_dir)
        lines = []
        for item in contents:
            full_path = os.path.join(target_dir, item)
            size = os.path.getsize(full_path) #bytes
            is_dir = os.path.isdir(full_path) #bool
            lines.append(f"- {item}: file_size ={size} bytes, is_dir={is_dir}")

        result = "\n".join(lines)
        return result
    except Exception as e:
        return f"Error: {e}"
