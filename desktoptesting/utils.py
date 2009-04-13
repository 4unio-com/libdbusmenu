import os

def enable_a11y(enable):
    os.environ['NO_GAIL'] = str(int(not enable))
    os.environ['NO_AT_BRIDGE'] = str(int(not enable))

def get_system_language():
    raise NotImplementedError, "not yet..."
