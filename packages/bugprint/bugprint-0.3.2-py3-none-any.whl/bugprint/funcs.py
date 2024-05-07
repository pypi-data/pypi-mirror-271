import os
import inspect

v = False

def bp_setup(verbose=False):
    global v
    v = verbose

def bp():
    caller_frame = inspect.currentframe().f_back
    caller_info = inspect.getframeinfo(caller_frame)
    relative_filename = os.path.relpath(caller_info.filename)
    resp = f"DEBUG: {relative_filename}:{caller_info.lineno} "

    if v:
        resp = resp + "-" * (80 - len(relative_filename) - len(str(caller_info.lineno)) - len("DEBUG: "))

    print(resp)
