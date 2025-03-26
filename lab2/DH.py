#algorytm Diffiego-Hellmana

import math
import random

def generate_prime():
    while True:
        n = random.randint(1000, 999999)
        if is_prime(n):
            return n

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

def find_primitive(n):
    required_set = set(range(1, n)) #zbiór {1, 2, ..., n-1}
    for g in range(2, n): 
        actual_set = set(pow(g, i, n) for i in range(1, n))
        if required_set == actual_set:
            return g
    raise ValueError("Nie znaleziono pierwiastka pierwotnego")
        
def diffie_helmann(n, g):
    x = random.randint(1000, n)
    X = pow(g, x, n)
    y = random.randint(1000, n)
    Y = pow(g, y, n)
    print(f"Wartość X: {X}")
    print(f"Wartość Y: {Y}")
    shared_key_A = pow(Y, x, n)
    shared_key_B = pow(X, y, n)

    assert shared_key_A == shared_key_B

    return shared_key_A



if __name__ == "__main__":
    n = generate_prime()
    g = find_primitive(n)
    print(f"Wygenerowana losowa liczba pierwsza n: {n}")
    print(f"Wygenerowany losowy pierwiastek pierwotny g modulo n: {g}")
    session_key = diffie_helmann(n, g)
    print(f"Wygenerowany klucz sesji: {session_key}")
