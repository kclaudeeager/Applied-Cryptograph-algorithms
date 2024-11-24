import unittest
from RSA import *
class TestRSAFunctions(unittest.TestCase):

    def test_is_composite(self):
        self.assertTrue(is_composite(4))
        self.assertTrue(is_composite(9))
        self.assertFalse(is_composite(2))
        self.assertFalse(is_composite(17))

    def test_test_primality(self):
        self.assertTrue(test_primality(2))
        self.assertTrue(test_primality(17))
        self.assertFalse(test_primality(4))
        self.assertFalse(test_primality(9))

    def test_test_primality_v2(self):
        self.assertTrue(test_primality_v2(2))
        self.assertTrue(test_primality_v2(17))
        self.assertFalse(test_primality_v2(4))
        self.assertFalse(test_primality_v2(9))

    def test_generate_primes(self):
        primes = generate_primes(10)
        self.assertEqual(primes, [2, 3, 5, 7])
        primes = generate_primes(20)
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19])

    def test_generate_random_number(self):
        num = generate_random_number(1, 10)
        self.assertTrue(1 <= num <= 10)

    def test_could_be_prime(self):
        self.assertTrue(could_be_prime(5))
        self.assertTrue(could_be_prime(7))
        self.assertFalse(could_be_prime(8))
        self.assertFalse(could_be_prime(9))

    def test_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(101, 10), 1)
        self.assertEqual(gcd(54, 24), 6)

    def test_iterative_gcd(self):
        self.assertEqual(iterative_gcd(48, 18), 6)
        self.assertEqual(iterative_gcd(101, 10), 1)
        self.assertEqual(iterative_gcd(54, 24), 6)

    def test_EulerTotient(self):
        result, gcds = EulerTotient(12)
        self.assertEqual(result, 4)
        self.assertEqual(gcds, [1, 5, 7, 11])
        result, gcds = EulerTotient(15)
        self.assertEqual(result, 8)
        self.assertEqual(gcds, [1, 2, 4, 7, 8, 11, 13, 14])

    def test_test_euler_totient(self):
        test_euler_totient(3, 11)  # 3 and 11 are primes, so (3-1)*(11-1) = 2*10 = 20
        test_euler_totient(5, 7)   # 5 and 7 are primes, so (5-1)*(7-1) = 4*6 = 24

if __name__ == '__main__':
    unittest.main()