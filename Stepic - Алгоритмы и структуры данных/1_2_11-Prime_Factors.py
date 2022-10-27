# https://stepik.org/lesson/12555/step/11
#
# Выведите разложение натурального числа n > 1 на простые множители. Простые множители должны быть упорядочены по возрастанию и разделены пробелами.
#
# Sample Input:
#   75
# 
# Sample Output:
#   3 5 5
# 

def devisors(number: int) -> list:
    """
    Return sorted in accending order list of <number> devisors
    """
    from math import sqrt

    if number < 2:
        return []

    _lesser_devisors = []
    _greater_devisors = []

    for possible_devisor in range(1, int(sqrt(number)) + 1):
        if number % possible_devisor == 0:
            _lesser_devisors.append(possible_devisor)
            if possible_devisor != number // possible_devisor:
                _greater_devisors.append(number // possible_devisor)

    return _lesser_devisors + _greater_devisors[::-1]

_prime_cash = {}
def is_prime(number: int) -> bool:
    """
    Return True if <number> is prime else False
    """
    try:
        _prime_cash.keys()
    except NameError:
        _prime_cash = {}

    if number in _prime_cash:
        result = _prime_cash[number]
    else:
        result = len(devisors(number)) == 2 
        _prime_cash[number] = result

    return result

def prime_factors(number: int) -> list:
    """
    Return prime factors of <number>
    """
    if number < 2:
        return []

    factors = []
    probe = 1
    while number != 1:
        probe += 1
        if not is_prime(probe):
            continue
        while number % probe == 0:
            number = number // probe
            factors.append(probe)
    return factors

if __name__ == "__main__":
    # n = int(input())
    n = 1234145124
    print(*prime_factors(n))