import random
from etc.hashing import sha2_to_int
from etc.prime import factorize, random_prime, is_prime
from etc.modulo import powermod
from etc.extendedeuclidian import extendedEuclidian, moduloInverse

A = 88 
B = 20

print(f"A: {A} B: {B}") 


class Task1:
    def __init__(self):
        print("=== Task 1:")
        self.prime = self._choose_prime()
        self.factors = self._factorize_totient()
        self.alpha = self._choose_alpha()
        self.publicA = self._public_component(A, 'A')
        self.publicB = self._public_component(B, 'B')
        print()
        print(f"Assumption of public parts exchange. A receives {self.publicB}, B receives {self.publicA}.")
        self.sharedA = self._shared_component(self.publicB, 'PublicB', A, 'A')
        self.sharedB = self._shared_component(self.publicA, 'PublicA', B, 'B')
        print()
        print(f"Diffie-Hellman key exchange finished. Calculated shared key is {self.sharedA}.")

    def _choose_prime(self):
        prime = random_prime(max(A, B), 500)

        print()
        print("== Choosing prime p")
        print(f"Chosen prime p: {prime}")

        return prime

    def _choose_alpha(self):
        print()
        print("== Choosing primitive root α")
        for alpha in random.sample(range(1, self.prime), self.prime - 1):
            gcd = extendedEuclidian(alpha, self.prime).gcd 

            print()
            print(f"Picking α = {alpha}. Checking if it is a primitive root:")
            print(f"GCD({alpha}, {self.prime}) = {gcd}.")

            if gcd == 1:
                print(f"{alpha} and {self.prime} are relatively prime and as such, α = {alpha} could be a primitive root.")
                if self._is_primitive_root(alpha):
                    return alpha
            else:
                print(f"{alpha} and {self.prime} are not relatively prime and as such, α = {alpha} cannot be a primitive root.")

    def _factorize_totient(self):
        factors = factorize(self.prime - 1)

        print()
        print("== Factorizing φ(p - 1)")
        print(f"Factorization of φ(p - 1) = φ({self.prime - 1}) = {factors}")

        return factors

    def _is_primitive_root(self, alpha):
        print()
        print(f"== Checking if α = {alpha} is primitive root")
        for factor in self.factors[:-1]:
            power = powermod(alpha, factor, self.prime)
            print(f"Calculating α^f mod p = {alpha}^{factor} mod {self.prime} = {power}")
            if power == 1:
                print(f"As {alpha}^{factor} mod {self.prime} = {power}, α = {alpha} is not a primitive root!")
                return False
        print(f"None of the factor powers produced 1, as such α = {alpha} is a primitive root!")
        return True

    def _public_component(self, private, name):
        print()
        print(f"== Calculating public component {name}")

        public = powermod(self.alpha, private, self.prime)
        print(f"Calculating α^{name} mod p = {self.alpha}^{private} mod {self.prime} = {public}")
        return public

    def _shared_component(self, public, public_name, private, private_name):
        print()
        print("== Calculating shared component")

        shared = powermod(public, private, self.prime)
        print(f"Calculating {public_name}^{private_name} mod p = {public}^{private} mod {self.prime} = {shared}")
        return shared

class Task2:
    def __init__(self):
        print("=== Task 2:")
        self.prime_p, self.prime_q = self._choose_primes()
        self.n, self.totient = self._calculate_parameters()
        self.encryption_key, self.decryption_key = self._choose_private_key()
        print()
        print(f"Public key ({self.encryption_key}, {self.n}), private key ({self.decryption_key}, {self.n}).")
        self.encrypted_message = self._encrypt(A, 'A')
        self.decrypted_message = self._decrypt(self.encrypted_message, 'C')
        print()
        print("RSA encryption/decryption performed successfully.")
        print(f"Message = {A}, Encrypted Message = {self.encrypted_message}, Decrypted Message = {self.decrypted_message}.")

    def _choose_primes(self):
        primes = (random_prime(max(A, B), 500), random_prime(max(A, B), 500)) 

        print()
        print(f"== Choosing primes p, q")
        print(f"Chosen primes (p, q): {primes}")

        return primes

    def _calculate_parameters(self):
        n = self.prime_p * self.prime_q 
        totient = (self.prime_p - 1) * (self.prime_q - 1)

        print()
        print(f"== Calculating RSA parameters n, φ(n)")
        print(f"n = p * q = {self.prime_p} * {self.prime_q} = {n}")
        print(f"φ({n}) = (p - 1) * (q - 1) = {totient}")

        return (n, totient)

    def _choose_private_key(self):
        print()
        print(f"== Choosing keys e, d")
        for encrypytion_key in random.sample(range(1, self.totient), self.totient - 1):
            euclidian = extendedEuclidian(encrypytion_key, self.totient)
            print()
            print(f"Trying encryption key e = {encrypytion_key}. GCD(e, φ) = {euclidian.gcd}.")

            if euclidian.gcd == 1:
                decryption_key = moduloInverse(encrypytion_key, self.totient)

                print(f"GCD(e, φ) is 1, e = {encrypytion_key} is valid as a private key.")
                print(f"Derived decryption key d = e^(-1) = {decryption_key}.")

                return (encrypytion_key, decryption_key)

            print(f"GCD(e, φ) is not 1, e = {encrypytion_key} is not valid as a private key.")

    def _encrypt(self, message, name):
        ciphertext = powermod(message, self.encryption_key, self.n)

        print()
        print(f"== Encrypting {name} = {message}, using public key ({self.encryption_key}, {self.n}).")
        print(f"C = {name}^e mod n = {message}^{self.encryption_key} mod {self.n} = {ciphertext}.")

        return ciphertext

    def _decrypt(self, message, name):
        plaintext = powermod(message, self.decryption_key, self.n)

        print()
        print(f"== Decrypting {name} = {message}, using private key ({self.decryption_key}, {self.n}).")
        print(f"M = {name}^e mod n = {message}^{self.decryption_key} mod {self.n} = {plaintext}.")

        return plaintext

class Task3:

    def __init__(self, prime, alpha, private, public):
        print("=== Task 3:")
        print()
        print(f"== Using values that were generated during Task 1:")
        print(f"p = {prime}, α = {alpha}, private = {private}, public = {public}")
        self.prime = prime
        self.alpha = alpha
        self.private = private
        self.public = public

        self.ephemeral_key, self.inverse_ephemeral_key = self._choose_ephemeral_key()
        self.signature_1, self.signature_2 = self._sign(B, 'B')
        self.verify_1, self.verify_2 = self._verify(B, 'B')
        print()
        print(f"Signature (S1, S2) = ({self.signature_1}, {self.signature_2}) verified successfully: V1 == V2 -> {self.verify_1} == {self.verify_2} ({self.verify_1 == self.verify_2})")

    def _choose_ephemeral_key(self):
        print()
        print(f"== Choosing ephemeral key:")
        for ephemeral_key in random.sample(range(1, self.prime - 1), self.prime - 2):
            euclidian = extendedEuclidian(ephemeral_key, self.prime - 1)

            print()
            print(f"Trying ephemeral key k = {ephemeral_key}. GCD(k, p - 1) = {euclidian.gcd}.")

            if euclidian.gcd == 1:
                inverse_ephemeral_key = moduloInverse(ephemeral_key, self.prime - 1)

                print(f"GCD(k, p - 1) is 1, k = {ephemeral_key} is valid as an ephemeral key.")
                print(f"Derived inverse ephemeral key k^(-1) = {inverse_ephemeral_key}.")
                
                return (ephemeral_key, inverse_ephemeral_key)

            print(f"GCD(k, p - 1) is not 1, k = {ephemeral_key} is not valid an ephemeral key.")

    def _sign(self, message, name):
        print()
        print(f"== Signing message {name} = {message}.")
        signature_1 = powermod(self.alpha, self.ephemeral_key, self.prime)
        print(f"S1 = α^k mod p = {self.alpha}^{self.ephemeral_key} mod {self.prime} = {signature_1}")

        signature_2 = (self.inverse_ephemeral_key * (message - self.private * signature_1)) % (self.prime - 1)
        print(f"S2 = k^(-1) * ({name} - private * S1) mod (p - 1) = {self.inverse_ephemeral_key} * ({message} - {self.private} * {signature_1}) mod ({self.prime - 1}) = {signature_2}")

        return (signature_1, signature_2)

    def _verify(self, message, name):
        print()
        print(f"== Verifying signature (S1, S2) = ({self.signature_1}, {self.signature_2}).")

        verify_1 = powermod(self.alpha, message, self.prime)
        print(f"V1 = α^{name} mod p = {self.alpha}^{B} mod {self.prime} = {verify_1}")

        verify_2 = (powermod(self.public, self.signature_1, self.prime) * powermod(self.signature_1, self.signature_2, self.prime)) % self.prime
        print(f"V2 = public^S1 * S1^S2 mod p = {self.public}^{self.signature_1} * {self.signature_1}^{self.signature_2} mod {self.prime} = {verify_2}")
        return (verify_1, verify_2)


class Bonus1:
    def __init__(self, prime, alpha, private, public, signature_1, signature_2, ephemeral_key, inverse_ephemeral_key):
        print("=== Bonus 1:")
        print("NOTE: Given that solutions exist only for specific inputs, re-ran the code, until the parameter choices yielded an answer.")
        print()
        print(f"== Using values that were generated during Task 1:")
        print(f"p = {prime}, α = {alpha}, private = {private}, public = {public}")
        print()
        print(f"== Using values that were generated during Task 3:")
        print(f"(Task3_S1, Task3_S2) = ({signature_1}, {signature_2}), k = {ephemeral_key}, k^(-1) = {inverse_ephemeral_key}")

        self.M = 13
        self.prime = prime
        self.alpha = alpha
        self.private = private
        self.public = public
        self.task3_signature_1 = signature_1
        self.task3_signature_2 = signature_2
        self.ephemeral_key = ephemeral_key
        self.inverse_ephemeral_key = inverse_ephemeral_key


        self.signature_1, self.signature_2 = self._sign(self.M, 'M')
        self.recovered_ephemeral_key = self._recover_ephemeral_key()
        self.recovered_secret = self._recover_secret()
        print()
        print(f"Ephemeral key was {self.ephemeral_key}, recovered ephemeral key was {self.recovered_ephemeral_key}.")
        print(f"Secret was {self.private}, recovered secret was {self.recovered_secret}.")


    def _sign(self, message, name):
        print()
        print(f"== Signing message {name} = {message}.")
        signature_1 = powermod(self.alpha, self.ephemeral_key, self.prime)
        print(f"S1 = α^k mod p = {self.alpha}^{self.ephemeral_key} mod {self.prime} = {signature_1}")

        signature_2 = (self.inverse_ephemeral_key * (message - self.private * signature_1)) % (self.prime - 1)
        print(f"S2 = k^(-1) * ({name} - private * S1) mod (p - 1) = {self.inverse_ephemeral_key} * ({message} - {self.private} * {signature_1}) mod ({self.prime - 1}) = {signature_2}")

        return (signature_1, signature_2)

    def _recover_ephemeral_key(self):
        print()
        print("== Attempting to recover ephemeral key")
        print("  Recovery formula derived from https://crypto.stackexchange.com/a/1520")
        print("  In addition, just having two ciphertexts that were signed using the same ephemeral key is not always enough.")
        print("  As per https://crypto.stackexchange.com/a/1520, we only have a solution if GCD(Task3_S2 - S2, p - 1) = 1, as we are required to calculate inverse of (Task3_S2 - S2).")
        gcd = extendedEuclidian(self.task3_signature_2 - self.signature_2, self.prime - 1).gcd
        if gcd != 1:
            print(f"GCD(Task3_S2 - S2, p - 1) = GCD({self.task3_signature_2 - self.signature_2}, {self.prime - 1}) = {gcd}, as such ephemeral key cannot be recovered!")
            return None
        print(f"GCD(Task3_S2 - S2, p - 1) = GCD({self.task3_signature_2 - self.signature_2}, {self.prime - 1}) = {gcd}, as such ephemeral key can be recovered!")

        recovered_ephemeral_key = ((B - self.M) * moduloInverse(self.task3_signature_2 - self.signature_2, self.prime - 1)) % (self.prime - 1)
        print(f"k = (Task3_Message - Bonus_Message) * (Task3_S2 - S2)^(-1) mod (p - 1) = ({B} - {self.M}) * ({self.task3_signature_2} - {self.signature_2})^(-1) mod ({self.prime - 1}) = {recovered_ephemeral_key}")
        return recovered_ephemeral_key

    def _recover_secret(self):
        print()
        print("== Attempting to recover secret key")
        if not self.recovered_ephemeral_key:
            print("Without recovered ephemeral key secret cannot be recovered!")
            return None
            
        print("  Recovery formula derived from https://crypto.stackexchange.com/a/1520")
        print("  In addition, just having two ciphertexts that were signed using the same ephemeral key is not always enough.")
        print("  As per https://crypto.stackexchange.com/a/1520, we only have a solution if GCD(S1, p - 1) = 1, as we are required to calculate inverse of S1.")
        
        gcd = extendedEuclidian(self.signature_1, self.prime - 1).gcd
        if gcd != 1:
            print(f"GCD(S1, p - 1) = GCD({self.signature_1}, {self.prime - 1}) = {gcd}, as such secret cannot be recovered!")
            return None
        print(f"GCD(S1, p - 1) = GCD({self.signature_1}, {self.prime - 1}) = {gcd}, as such secret can be recovered!")

        recovered_secret = ((self.M - self.ephemeral_key * self.signature_2) * moduloInverse(self.signature_1, self.prime - 1)) % (self.prime - 1)
        print(f"s = (M - k * S2) * S1^(-1) mod (p - 1) = ({self.M} - {self.ephemeral_key} * {self.signature_2}) * {self.signature_1}^(-1) mod {self.prime - 1} = {recovered_secret}")
        return recovered_secret

class Bonus2:
    def __init__(self):
        print("=== Bonus 2:")
        print("We need to select a generator value in a multiplicative integer group.")
        print("By Little Fermat Theorem, we have g^q = h^(r*q) = h^(p - 1) = 1 mod p.")
        print("To do so, we start by picking a random prime q. Then we calculate r = 2, p = 2*q + 1 and check if it is prime.")
        print("If p is prime, then our generator is calculated by picking a random value h and calulating g = h^2.")
        print("If g is not equal to 1, g is a generator for multiplicative integer group of base p.")
        self.prime_p, self.prime_q = self._choose_primes()
        self.generator = self._choose_generator()
        self.private_key, self.public_key = self._choose_keys()
        self.signature_1, self.signature_2 = self._sign(B, 'B')
        self.verify_1, self.verify_2 = self._verify(B, 'B')

        print(f"Signature (S1, S2) = ({self.signature_1}, {self.signature_2}) verified successfully: S1 == V2 -> {self.signature_1} == {self.verify_2} ({self.signature_1 == self.verify_2})")

    def _choose_primes(self):
        print()
        print(f"== Choosing primes")
        while True:
            prime_q = random_prime(max(A, B), 100)
            prime_p = 2 * prime_q + 1

            print(f"Chosen prime q: {prime_q}")
            print(f"p = 2 * q + 1 = 2 * {prime_q} + 1 = {prime_p}")

            if is_prime(prime_p):
                print(f"p = {prime_p} is a prime number.")
                return prime_p, prime_q

            print(f"p = {prime_p} is not a prime number.")

    def _choose_generator(self):
        print()
        print(f"== Choosing generator")
        while True:
            h = random.randint(1, self.prime_p - 1)
            g = powermod(h, 2, self.prime_p)

            print(f"Chosen h: {h}")
            print(f"g = h^r mod p = {h}^2 mod {self.prime_p} = {g} ")

            if g != 1:
                print(f"g = {g} is a generator of multiplicative integer group of order {self.prime_q}.")
                return g

            print(f"g = {g} is not a generator of multiplicative integer group of order {self.prime_q}.")

    def _choose_keys(self):
        private_key = random.randint(1, self.prime_q)
        public_key = powermod(self.generator, private_key, self.prime_q)

        print()
        print(f"== Choosing keys")
        print(f"Chosen private key x: {private_key}")
        print(f"Public key y = g^x = {self.generator}^{private_key} = {public_key}")

        return private_key, public_key

    def _sign(self, message, name):

        ephemeral_key = random.randint(1, self.prime_q)
        signature_1 = sha2_to_int(str(message) + str(powermod(self.generator, ephemeral_key, self.prime_q))) % self.prime_q
        signature_2 = (ephemeral_key - self.private_key * signature_1) % (self.prime_q - 1)

        print()
        print(f"== Signing message {name} = {message}")
        print(f"Chosen ephemeral key k: {ephemeral_key}")
        print(f"S1 = H(M || g^k) = H({message} || {self.generator}^{ephemeral_key}) = H({message} || {powermod(self.generator, ephemeral_key, self.prime_q)}) = {signature_1}")
        print(f"S2 = (k - xe) mod (q - 1) = ({ephemeral_key} - {self.private_key} * {signature_1}) mod {self.prime_q - 1} = {signature_2}")
        print(f"Signature of {name} = {message} is {signature_1, signature_2}.")

        return signature_1, signature_2
    
    def _verify(self, message, name):
        
        validation_1 = (powermod(self.generator, self.signature_2, self.prime_q) * powermod(self.public_key, self.signature_1, self.prime_q)) % self.prime_q
        validation_2 = sha2_to_int(str(message) + str(validation_1)) % self.prime_q

        print()
        print(f"== Verifying signature {self.signature_1, self.signature_2} of message {name} = {message}")
        print(f"V1 = g^S2 * y^S1 = {self.generator}^{self.signature_2} * {self.public_key}^{self.signature_1} = {validation_1}")
        print(f"V2 = H(M || r) = H({message} || {validation_1}) = {validation_2}")

        return validation_1, validation_2


task1 = Task1()

print()
task2 = Task2()

print()
task3 = Task3(task1.prime, task1.alpha, A, task1.publicA)

print()
bonus1 = Bonus1(task1.prime, task1.alpha, A, task1.publicA, task3.signature_1, task3.signature_2, task3.ephemeral_key, task3.inverse_ephemeral_key)

print()
bonus2 = Bonus2()
