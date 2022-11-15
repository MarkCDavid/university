def is_prime(i):
    for j in range(2, i):
        if i % j == 0:
            return False
    return True

for i in range(100, 1000):
    if is_prime(i):
        j = (i - 1) // 2
        if is_prime(j):
            pass #print(i)


n = 503

a = 62
for j in range(1, 503):
    _a = (a ** j) % n
    if j == 502 and _a == 1:
        print("root")
    elif _a == 1:
        print("not root")


