import fact
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
    print("Factorial")
    for n in range(0,990,30):
        print("n={}\tt_rec={:.6f}\tt_iter={:.6f}".format(
            n,
            timed_call(fact.fact,n),
            timed_call(fact.fact_iterative,n)
        ))
