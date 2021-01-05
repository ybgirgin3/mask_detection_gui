import os
from elevate import elevate

def is_root():
    return os.getuid() == 0

print("before ", is_root())

# to prevent graphical on linux but gets it from terminal screen
# elevate(graphical=False)

# to suppress the new windos on windows
# elevate(show_console=False)

elevate()
print("after ", is_root())
