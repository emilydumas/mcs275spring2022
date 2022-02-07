"Fibonacci numbers computed by recursion"
# MCS 275 Spring 2022 Lecture 12

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

# TODO: Explore ways to make this more efficient.