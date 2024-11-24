import argparse
import random
import matplotlib.pyplot as plt
import sys
from RSA import * # Import all functions from RSA module
import RSA
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run RSA functions or experiments.")
    parser.add_argument('--function', type=str, help="Function name to run")
    parser.add_argument('--check_available_functions', action='store_true', help="Check available functions")
    parser.add_argument('--data', type=str, help="Data to pass to the function (comma-separated)")
    args = parser.parse_args()
    
    if args.check_available_functions:
        print("Available functions to test:")
        # Print the available functions
        for func in dir(RSA):
            if not func.startswith("__"):
                print(f"  {func}")
        exit(0)
        
    if args.function and args.data:
        # Parse the data argument
        data = [eval(x) for x in args.data.split(',')]
        # Get the function
        function = globals().get(args.function)
        if function:
            # Call the function with the provided data
            result = function(*data)
            print(f"Result of {args.function}({', '.join(args.data.split(','))}): {result}")
        else:
            print(f"Function {args.function} not found.")
    else:
        # Generate a random number in the interval 5 million to 6 million
        n = generate_random_number(5*10**6, 6*10**6)
        print(n)

        results = []

        for i in range(1000):
            count = 0
            n = generate_random_number(5*10**6, 6*10**6)
            while not test_primality_v2(n):
                n = generate_random_number(5*10**6, 6*10**6)
                count += 1
            results.append(count)
        average = sum(results) / len(results)
        print("Average for range 5 million to 6 million:", average)

        # Now for the range 500 billion to 500 billion plus 1 million
        results = []
        five_billion = 5*10**11

        for i in range(250):
            count = 0
            n = generate_random_number(five_billion, five_billion + 10**6)
            while not test_primality_v2(n):
                n = generate_random_number(five_billion, five_billion + 10**6)
                count += 1
            results.append(count)
        average = sum(results) / len(results)
        print("Average for range 500 billion to 500 billion plus 1 million:", average)

        # Check if a number fits the 6k ± 1 rule
        could_be_prime = lambda n: n == 2 or n == 3 or (n > 3 and (n % 6 == 1 or n % 6 == 5))

        # Calculate the percentage of primes up to each N in [5000, 5000000]
        prime_counts = []
        N_values = []
        prime_count = 0

        for N in range(5000, 5000001):
            if could_be_prime(N) and test_primality_v2(N):
                prime_count += 1
            # Record every 1000 steps
            if N % 1000 == 0:
                prime_counts.append(100 * prime_count / N)
                N_values.append(N)

        # Plot the results
        # Plot the results with log scale on the x-axis
        plt.figure(figsize=(10, 6))
        plt.plot(N_values, prime_counts)
        plt.xlabel("N (range [1, N]) in steps of 1000 (log scale)")
        plt.xscale("log")  # Apply logarithmic scale to x-axis
        plt.ylabel("Percentage of primes in range [1, N]")
        plt.title("Prime Density as N Increases")
        plt.grid(True)
        # save the plot to a file
        plt.savefig("prime_density.png")
        
        #Find 2 prime numbers between 2000 and 3000
        primes = []
        for i in range(2000, 3001):
            if could_be_prime(i) and test_primality_v2(i):
                primes.append(i)
        print(primes)

        # Take two numbers from the list of primes
        p, q = primes[0], primes[1]
        n = p * q
        print(n)
        # Calculate Euler's totient function for n
        p_q_euler_result,_ = EulerTotient(n)
        print("p_q_euler: ",p_q_euler_result) # Should be (p-1)*(q-1)
        assert p_q_euler_result == (p-1)*(q-1)
        print("p-1: ",p-1)
        print("q-1: ",q-1)
        print("p-1 * q-1: ",(p-1)*(q-1))

        # Test it for a few combinations of p and q

        # Choose a ranom cominations of p and q from primes
        pqs= [random.sample(primes, 2) for _ in range(10)]
        print(pqs)
        
        
        # Write the test function for Euler's totient function
        def test_euler_totient(p, q):
            n = p * q
            p_q_euler_result,_ = EulerTotient(n)
            assert p_q_euler_result == (p-1)*(q-1)
            print(f"Test passed for p = {p} and q = {q}")

        # Test the function for the 10 combinations of p and q
        for p, q in pqs:
            test_euler_totient(p, q)
    
        '''
        Test passed for p = 2617 and q = 2879
        Test passed for p = 2141 and q = 2531
        Test passed for p = 2699 and q = 2281
        Test passed for p = 2693 and q = 2069
        Test passed for p = 2069 and q = 2473
        Test passed for p = 2281 and q = 2557
        Test passed for p = 2917 and q = 2161
        Test passed for p = 2663 and q = 2803
        Test passed for p = 2753 and q = 2399
        Test passed for p = 2179 and q = 2887
        '''
        
        