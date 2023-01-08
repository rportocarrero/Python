def taylor_series(function, x0, n):
    """
    Compute the Taylor series expansion of the function around the point x0.

    Parameters:
    function (callable): The function to approximate.
    x0 (float): The point around which to expand the function.
    n (int): The number of terms in the expansion.

    Returns:
    float: The approximation of the function using the first n terms of the Taylor series expansion.
    """
    # Initialize the approximation to the first term of the expansion
    approximation = function(x0)

    # Initialize the factor to 1 and the exponent to 1
    factor = 1
    exponent = 1

    # Loop through the terms of the expansion and update the approximation
    for i in range(n-1):
        factor *= -1 / (exponent + 1)
        exponent += 1
        approximation += factor * function(x0 + exponent)

    return approximation

def func(x):
    return x**2

print(taylor_series(func, 0,10))