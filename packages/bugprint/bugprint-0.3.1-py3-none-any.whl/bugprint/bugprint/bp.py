import os
import inspect

def bp():
    caller_frame = inspect.currentframe().f_back
    caller_info = inspect.getframeinfo(caller_frame)
    filename = caller_info.filename
    relative_filename = os.path.relpath(filename)
    print(f"BP DEBUG: {relative_filename}, line {caller_info.lineno}")
