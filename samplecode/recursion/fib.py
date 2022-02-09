"Fibonacci numbers computed by recursion"
# MCS 275 Spring 2022 Lecture 12
import decs

@decs.count_calls
def fib(n):
    """
    Return the nth Fibonacci number using a
    shockingly inefficient, naive recursive
    algorithm.
    """
    if n<0:
        raise ValueError("This function only supports computation of F_n for n>=0")
    if n<=1:
        # F_0 = 0 and F_1 = 1
        return n
    # Otherwise, F_n = F_{n-1} + F_{n-2}
    return fib(n-1) + fib(n-2)

@decs.count_calls
def fib_iterative(n):
    """
    Return the nth Fibonacci number using an
    iterative method.
    """
    if n<0:
        raise ValueError("This function only supports computation of F_n for n>=0")
    if n<=1:
        # F_0 = 0 and F_1 = 1
        return n
    a,b = 0,1  # F_0, F_1
    for _ in range(n-1):
        a,b = b,a+b  # replace F_{k-1}, F_k 
                     # with F_k, F_{k+1}
    return b
