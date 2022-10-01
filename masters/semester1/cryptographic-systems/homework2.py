from etc.extendedeuclidian import extendedEuclidian

A = "AurimasSakalys"
B = 20185388
C = "VILNIUSGEDIMINASTECHNIKALUNIVERSITY"

B1 = 2018
B2 = 5388

print("=== Task 1:")

t1_result = extendedEuclidian(B1, B2)
print(f"GCD({B1}, {B2}) is {t1_result.gcd}")

print("=== Task 2:")

t2_result = extendedEuclidian(B, 661)
print(f"Multiplicative inverse of {B} is {t2_result.bezout[0] % 661}")