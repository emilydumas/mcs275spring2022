"Factorial function"
# MCS 275 Spring 2022 Lecture 12

def fact(n):
    "Factorial of a nonnegative integer n"
    if n<0:
        raise ValueError("Factorial only defined for nonnegative integers")
    if n<=1:
        # 0! = 1! = 1
        return 1
    # n is at least two, so
    # n! = n * (n-1)!
    return n * fact(n-1)

def fact_iterative(n):
    "Factorial, but computed iteratively"
    # TODO: add this
