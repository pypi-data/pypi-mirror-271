import inspect


def findPermutations(target_product):
    """
    Generate permutations of two numbers
    where their product is less than
    the target product.
    """
    for s in range(2, target_product + 2):
        for i in range(1, s):
            j = s - i
            product = i * j
            if product <= target_product:
                yield (i, j)


def numArguments(func):
    """
    Returns the number of arguments required by a function.
    """
    signature = inspect.signature(func)
    return sum(
            1 for param in signature.parameters.values()
            if param.default == inspect.Parameter.empty
            )
