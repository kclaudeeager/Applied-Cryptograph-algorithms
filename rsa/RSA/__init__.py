# __init__.py
from .rsa import RSA

__all__ = [
    'is_composite',
    'test_primality',
    'test_primality_v2',
    'generate_primes',
    'generate_random_number',
    'could_be_prime',
    'gcd',
    'iterative_gcd',
    'EulerTotient',
    'test_euler_totient'
]

is_composite = RSA.is_composite
test_primality = RSA.test_primality
test_primality_v2 = RSA.test_primality_v2
generate_primes = RSA.generate_primes
generate_random_number = RSA.generate_random_number
could_be_prime = RSA.could_be_prime
gcd = RSA.gcd
iterative_gcd = RSA.iterative_gcd
EulerTotient = RSA.EulerTotient
test_euler_totient = RSA.test_euler_totient