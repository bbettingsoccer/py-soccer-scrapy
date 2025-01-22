import os
import sys
import inspect

def get_project_root_dir():
    frame_info = inspect.stack()[1]
    caller_path = frame_info.filename
    caller_absolute_path = os.path.abspath(caller_path)
    paths = [p for p in sys.path if p in caller_absolute_path]
    paths.sort(key=lambda p: len(p))
    caller_root_path = paths[0]
    return caller_root_path

print(get_project_root_dir())