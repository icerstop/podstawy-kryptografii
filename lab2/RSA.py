#algorytm RSA

import math
import random

def generate_prime():
    while True:
        n = random.randint(1000, 9999) #tylko liczby czterocyfrowe
        if is_prime(n):
            return n
        
def generate_two_primes():
    p = generate_prime()
    q = generate_prime()
    while abs(p - q) < 3000: #minimalna różnica między p i q wynosi 3000
        q = generate_prime()
    return p, q

def generate_e(phi):
    while True:
        e = random.randint(2, phi - 1) #e musi być mniejsze od phi
        if math.gcd(e, phi) == 1: #e i phi są względnie pierwsze
            return e

def generate_d(e, phi):
    return pow(e, -1, phi)
        

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

def encrypt(message: str, public_key: tuple[int,int]) -> list[int]:
    e, n = public_key
    message_bytes = message.encode('utf-8') #każdy bajt z przedziału 0-255, więc na pewno jest mniejszy od n, bo n = p*q (obie to liczby czterocyfrowe)
    return [pow(b, e, n) for b in message_bytes] #dla każdego bajtu c = b^e mod n

def decrypt(cipher: list[int], private_key: tuple[int,int]) -> str:
    d, n = private_key
    decrypted_bytes = [pow(c, d, n) for c in cipher] #dla każdego bajtu m = c^d mod n
    return bytes(decrypted_bytes).decode('utf-8') #odtworzenie oryginalnej wiadomości i dekod do utf-8



if __name__ == "__main__":
    p, q = generate_two_primes()
    print("p:", p)
    print("q:", q)
    n = p * q
    phi = (p - 1) * (q - 1)
    print("phi:", phi)
    e = generate_e(phi)
    print("e:", e)
    d = generate_d(e, phi)
    print("d:", d)
    public_key = (e, n)
    private_key = (d, n)
    print("Klucz publiczny:", public_key)
    print("Klucz prywatny:", private_key)
    message = "Lorem ipsum dolor sit amet consectetur adipiscing."
    cipher = encrypt(message, public_key)
    print("Zaszyfrowana wiadomość:", cipher)
    decrypted_message = decrypt(cipher, private_key)
    print("Odszyfrowana wiadomość:", decrypted_message)

