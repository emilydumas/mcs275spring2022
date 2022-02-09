"Sample decorators"
# MCS 275 Spring 2022 Lectures 8-9

def twicify(f):
    "Decorator that replaces a function with one that does the same thing twice"
    def ftwice(*args,**kwargs):
        f(*args,**kwargs)
        return f(*args,**kwargs)
    return ftwice

def loggedcall(f):
    "Decorator that logs the start and end of each call"
    def inner(*args,**kwargs):
        print("About to call",f.__name__)
        retval = f(*args,**kwargs)
        print("Finished call to",f.__name__)
        return retval
    return inner

call_counts = {} # empty dictionary
                 # will contain things like "print": 341
                 #                          "f": 11

def count_calls(f):
    "Decorator that records number of calls in a dictionary"
    def inner(*args,**kwargs):
        # record that f is being called
        if f.__name__ in call_counts:
            # not the first call, so just increase count by 1
            call_counts[f.__name__] += 1
        else:
            # first call, set the call count to 1
            call_counts[f.__name__] = 1
        # call f
        return f(*args,**kwargs)
        
    return inner # inner is basically f, but it also records the call!

def get_call_count(fname):
    "Retrieve the number of times function with given name was called"
    if fname in call_counts:
        return call_counts[fname]
    else:
        # Never called = 0 calls
        return 0

if __name__ == "__main__":
    # Demonstrate
    import time

    @twicify
    def g():
        print("This function was written to print once, with twicify decorator applied")

    @loggedcall
    def h():
        print("This is the function h")

    @loggedcall
    def count_up():
        for i in range(10):
            print(i+1)
            time.sleep(0.2)
    
    @count_calls
    def k(x):
        return x*x

    g()
    h()
    count_up()

    L = list(range(20))
    SQ = [ k(x) for x in L ]
    print("Got list of squares:",SQ)
    print("This involved",get_call_count("k"),"calls to function k")
