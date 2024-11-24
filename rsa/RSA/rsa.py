
import random
import math
import matplotlib.pyplot as plt

import random
import math
import matplotlib.pyplot as plt

class RSA:
    def __init__(self):
        pass

    @staticmethod
    def is_composite(n):
        if n <= 1:
            return False
        sqrt_n = int(n ** 0.5)
        for a in range(2, sqrt_n + 1):
            if n % a == 0:
                b = n // a
                if b <= sqrt_n:
                    return True
        return False

    @staticmethod
    def test_primality(n):
        if n == 1:
            return False
        if n == 2:
            return True
        num_sqrt = int(n ** 0.5)
        for a in range(2, num_sqrt + 1):
            if n % a == 0:
                return False
        return True

    @staticmethod
    def test_primality_v2(n):
        if n == 1:
            return False
        if n == 2:
            return True
        if n<=3:
            return True
        if n % 2 == 0:
            return False
        if n % 3 == 0:
            return False
        num_sqrt = int(n ** 0.5)
        if num_sqrt > 5:
            for a in range(num_sqrt, 4, -1):
                if n % a == 0:
                    return False
        return True

    @staticmethod
    def generate_primes(n):
        primes = []
        for i in range(2, n):
            if RSA.test_primality_v2(i):
                primes.append(i)
        return primes

    @staticmethod
    def generate_random_number(from_n, to_n):
        return random.randint(from_n, to_n)

    @staticmethod
    def could_be_prime(n):
        return n == 2 or n == 3 or (n > 3 and (n % 6 == 1 or n % 6 == 5))

    @staticmethod
    def gcd(a, b):
        if b == 0:
            return a
        return RSA.gcd(b, a % b)

    @staticmethod
    def iterative_gcd(a, b):
        while b != 0:
            q = a // b
            r = a % b
            a, b = b, r
        return a

    @staticmethod
    def EulerTotient(n):
        result = 1
        gcds = [1]
        for i in range(2, n):
            gcd = RSA.iterative_gcd(i, n)
            if gcd == 1:
                gcds.append(i)
                result += 1
        return result, gcds

    @staticmethod
    def test_euler_totient(p, q):
        n = p * q
        p_q_euler_result, _ = RSA.EulerTotient(n)
        assert p_q_euler_result == (p - 1) * (q - 1)
        print(f"Test passed for p = {p} and q = {q}")
