def find_N(d, p):
    """
    Estimate Sum(1 / n**p) from n = 1 to infinity.
    d = error bound (10**(-d))
    p = exponent in telescoping equation
    Finds N value needed to compute sum with error of d.
    """
    import math
    N = 10**(math.log(10**d / (p - 1), 10)/ (p - 1))
    N = math.ceil(N). # find nearest (larger) whole number
    print(f"N = {N}")
    return None

print("Example:")
find_N(5, 7)
