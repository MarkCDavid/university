import math

def is_prime(number: 'int') -> 'bool':
    if number <= 1:
        return False
    
    upper_bound = int(math.sqrt(number)) + 1

    for i in range(3, upper_bound):
        if number % i == 0:
            return False

    return True