def mod_pn(value: 'int', modulo: 'int') -> 'int':
    modulo = modulo // 2 
    for value_prime in range(-modulo, modulo):
        if value_prime % modulo == value % modulo:
            return value_prime

def mod_p(value: 'int', modulo: 'int') -> 'int':
    return value % modulo