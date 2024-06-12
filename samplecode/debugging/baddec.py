"""Decorator example with an error (for debugging)"""
# MCS 275 - Emily Dumas

def twice(f):
    """Decorator that replaces a function with a version
    that runs twice"""
    def inner(*args,**kwargs):
        """Call a certain function twice, returning the
        second result."""
        f(*args,**kwargs)
        return f(*args,**kwargs)
    return inner

def hello():
   """Print greeting"""
   print("Hello everyone!")

hello_twice = twice(hello())
hello_twice()
