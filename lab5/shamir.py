import secrets
import matplotlib.pyplot as plt

class Shamir:

    def __init__(self, p=None, bits=10):
        self.p = p or self._generate_large_prime()

    def _is_prime(self, n, k=5):
        if n < 2:
            return False
        for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
            if n % prime == 0 and n != prime:
                return False
        r, d = 0, n-1
        while d % 2 == 0:
            d //= 2
            r += 1

        for _ in range(k):
            a = secrets.randbelow(n-3) + 2
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def _generate_large_prime(self, bits = 10):
        while True:
            candidate = secrets.randbits(bits) | 1
            if candidate >= 1000 and candidate % 2 == 1 and self._is_prime(candidate):
                return candidate
            
    def split(self, secret, n , t):
        assert 1 < t <= n, "Treshold t musi być większy od 1 i mniejszy/równy n"
        assert secret < self.p, "Sekret musi być mniejszy od liczby pierwszej p"

        coeffs = [secret] + [secrets.randbelow(self.p) for _ in range(t-1)]

        shares = []
        for i in range(1, n+1):
            x = i
            y = sum(coeffs[j] * pow(x, j, self.p) for j in range(t)) % self.p
            shares.append((x, y))

        self.__coeffs = coeffs

        return shares

    def reconstruct(self, shares, t=None):
        if t is None:
            t = len(shares)

        secret = 0
        for i in range(t):
            x_i, y_i = shares[i]
            l_i = 1
            for j in range(t):
                if i != j:
                    x_j, _ = shares[j]
                    num = (self.p - x_j) % self.p
                    den = (x_i - x_j) % self.p
                    inv = pow(den, -1, self.p)
                    l_i = (l_i * num * inv) % self.p
            secret = (secret + y_i * l_i) % self.p
        return secret
    
    def visualize_shamir(self, shares):

        coeffs = self.__coeffs
        p = self.p

        x_vals = [x for x, _ in shares]
        y_vals = [y for _, y in shares]

        poly_x = list(range(1, max(x_vals) + 2))
        poly_y = [
            sum(coeffs[i] * pow(x, i, p) for i in range(len(coeffs))) % p for x in poly_x
        ]

        plt.figure(figsize=(10, 6))
        plt.plot(poly_x, poly_y, label="Wielomian (f(x))", linestyle='-', marker='.')
        plt.scatter(x_vals, y_vals, color='red', zorder=5, label="Udziały (punkty)")

        for x, y in shares:
            plt.text(x, y+2, f"({x}, {y})", ha='center', fontsize=8)

        plt.title("Wizualizacja algorytmu Shamira")
        plt.xlabel("x")
        plt.ylabel("y = f(x) mod p")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

# ------------------------------------------------------------
# Wyjaśnienie działania algorytmu Shamira i jego właściwości:
#
# Parametry konfigurowalne w aplikacji:
#   a) n – całkowita liczba udziałów (ang. shares),
#   b) t – liczba wymaganych udziałów do odtworzenia sekretu (prog),
#   c) s – sekret (liczba całkowita z przedziału [0, p-1]),
#   d) p – liczba pierwsza, wyznaczająca przestrzeń działań modulo.
#
# Jak działa algorytm?
#   ➤ Tworzony jest wielomian stopnia t-1, gdzie:
#       - wyraz wolny to sekret (a₀ = s),
#       - pozostałe współczynniki są losowe.
#   ➤ Obliczane są punkty tego wielomianu w n różnych miejscach (x),
#     i one stanowią udziały w postaci (x, f(x)).
#   ➤ Do rekonstrukcji sekretu wystarczy dowolne t punktów – używany
#     jest interpolacyjny wzór Lagrange’a do odzyskania wyrazu wolnego.
#
# Zabezpieczenia:
#   - Sekret jest doskonale ukryty, dopóki nie ma t udziałów.
#   - Posiadanie < t udziałów nie daje ŻADNEJ informacji o sekrecie.
#
# Minimalna liczba udziałów:
#   ➤ Minimalna liczba udziałów, by algorytm działał poprawnie, to t.
#   ➤ Jeśli dostarczymy mniej niż t punktów, interpolacja jest
#     matematycznie niemożliwa – uzyskujemy nieskończenie wiele rozwiązań.
#
# Uwagi praktyczne:
#   - Należy unikać zbyt małych wartości liczby pierwszej p (np. < 1000),
#     gdyż może to prowadzić do błędów przy obliczeniach odwrotności modulo.
#   - Dla bezpieczeństwa kryptograficznego zaleca się p ≥ 128 bitów.
#
# Funkcja visualize_shamir() pozwala zobaczyć na wykresie punkty udziałów
# oraz wykres wielomianu interpolującego (działającego w ℤₚ).
#
# ------------------------------------------------------------
