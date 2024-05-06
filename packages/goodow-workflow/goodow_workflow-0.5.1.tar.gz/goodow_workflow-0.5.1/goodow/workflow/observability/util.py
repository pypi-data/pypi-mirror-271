import os

def is_debug_development():
    return "PYCHARM_HOSTED" in os.environ
