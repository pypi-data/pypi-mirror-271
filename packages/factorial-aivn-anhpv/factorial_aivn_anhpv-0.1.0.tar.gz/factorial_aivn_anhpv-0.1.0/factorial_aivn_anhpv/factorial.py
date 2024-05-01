def fact(n):
    """
    To calculate the factorial of a number
    Args:
        n: an integer
    Returns:
        the factorial of n
    """
    if n<0:
        raise ValueError("The number must be non-negative")
    elif n==0 or n==1:
        return 1
    else:
        return n*fact(n-1)