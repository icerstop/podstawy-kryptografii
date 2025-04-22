from shamir import Shamir
from trivial import Trivial
import secrets

def main():
    print("=== Trivial Secret Sharing ===\n")

    k = int(input("Enter value of k (modulus): "))
    n = int(input("Enter number of shares (n): "))

    secret = secrets.randbelow(k)
    print(f"Randomly chosen secret (less than {k}): {secret}")

    triv = Trivial(k)
    shares = triv.split(secret, n)
    print(f"Generated shares: {shares}")

    recovered_secret = triv.reconstruct(shares)
    print(f"Recovered secret: {recovered_secret}\n")

    print("=== Shamir's Secret Sharing ===\n")

    bits = int(input("Enter number of bits for the prime number (e.g. 10): "))
    shamir = Shamir(bits=bits)

    n = int(input("Enter number of total shares (n): "))
    t = int(input("Enter threshold number of shares (t): "))
    p = shamir.p
    print(f"Generated prime number p = {p}")
    secret = secrets.randbelow(p)
    print(f"Randomly chosen secret (less than {p}): {secret}")

    shares = shamir.split(secret, n, t)
    print(f"Generated shares (x, y): {shares}")

    selected = shares[:t]
    print(f"\nSelected first {t} shares for reconstruction: {selected}")
    recovered_secret = shamir.reconstruct(selected)
    print(f"Recovered secret: {recovered_secret}")

    shamir.visualize_shamir(shares)

if __name__ == "__main__":
    main()
