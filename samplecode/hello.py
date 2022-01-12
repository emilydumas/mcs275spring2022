"Print a message to the terminal and exit"
# MCS 275 Spring 2022 Lecture 2

import sys
import os

print("Hello world!")
print("This is running under Python",sys.version)
print("The location of the Python interpreter is:",sys.executable)
print("The current working directory is:",os.getcwd())
