"Timing studies for recursive and iterative functions"
import fact
import pfs
import fib
import time

def timed_call(func,*args,**kwargs):
    """
    Call func(*args,**kwargs), ignoring its return value
    and returning its running time instead
    """
    t0 = time.time()
    func(*args,**kwargs)
    return time.time() - t0


if __name__ == "__main__":
    # This code only runs when the file is
    # a script.  If imported as a module, it
    # will not run.
    print("Factorial")
    for n in range(0,990,30):
        print("n={}\tt_rec={:.6f}\tt_iter={:.6f}".format(
            n,
            timed_call(fact.fact,n),
            timed_call(fact.fact_iterative,n)
        ))
    print("\n\n\n\n")
    print("Paper-folding sequence")
    for n in range(0,24):
        print("n={}\tt_rec={:.6f}\tt_iter={:.6f}".format(
            n,
            timed_call(pfs.pfs,n),
            timed_call(pfs.pfs_iterative,n)
        ))
    print("\n\n\n\n")
    print("Fibonacci sequence")
    for n in range(0,100,5):
        print("n={}\tt_rec={:.6f}\tt_iter={:.6f}".format(
            n,
            timed_call(fib.fib,n),
            timed_call(fib.fib_iterative,n)
        ))