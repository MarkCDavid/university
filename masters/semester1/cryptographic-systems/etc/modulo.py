
def powermod(base, to, modulo):
    result = 1
    while to > 0:
        if to % 2 == 1:
            result = (result * base) % modulo
        to = to // 2
        base = (base ** 2) % modulo
    return result % modulo