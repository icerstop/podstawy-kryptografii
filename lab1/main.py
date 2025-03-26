import random
from collections import Counter
import sympy as sp
from math import gcd

# Funkcja generate_prime() generuje liczbę pierwszą z przedziału określonego przez indeksy,
# wybierając tylko te liczby, które są postaci 4k+3 (czyli reszta z dzielenia przez 4 wynosi 3).
def generate_prime():
    while True:
        # Losowo wybieramy indeks w przedziale od 10000 do 50000,
        # a sp.prime() zwraca liczbę pierwszą odpowiadającą temu indeksowi.
        prime = sp.prime(random.randrange(10000, 50000))
        # Sprawdzamy, czy liczba pierwsza ma postać 4k+3 (czyli modulo 4 daje 3).
        if prime % 4 == 3:
            return prime

# Funkcja bbs_generator(n, length) implementuje generator pseudolosowy Blum-Blum-Shub (BBS).
# Parametry:
#   - n: iloczyn dwóch liczb pierwszych (moduł),
#   - length: liczba bitów do wygenerowania.
def bbs_generator(n, length):
    # Inicjujemy wartość początkową x losując 16-bitową liczbę.
    x = random.getrandbits(16)
    # Upewniamy się, że x jest względnie pierwsze z n (gcd(x, n) == 1),
    # aby zapewnić poprawne działanie generatora.
    while gcd(x, n) != 1:
        x = random.getrandbits(16)
    bits = []  # Lista na wygenerowane bity
    for _ in range(length):
        # Generujemy kolejny stan x poprzez podniesienie do kwadratu modulo n.
        x = (x ** 2) % n
        # Pobieramy najmłodszy bit (bit najmniej znaczący) i dodajemy go do listy.
        bits.append(x & 1)
    return bits

# Funkcja single_bits_test(bits) sprawdza, czy liczba jedynek w ciągu bitów mieści się w zadanym przedziale.
# Zakłada się, że dla idealnego ciągu o długości 20000 bitów liczba jedynek powinna być bliska 20000/2.
def single_bits_test(bits):
    # Suma bitów (jedynki) powinna być większa niż 9725 i mniejsza niż 10275.
    return 9725 < sum(bits) < 10275

# Funkcja runs_test(bits) wykonuje test serii (runs test) sprawdzający występowanie ciągów kolejnych zer lub jedynek.
def runs_test(bits):
    # Inicjalizujemy słownik dla długości serii od 1 do 6 dla obu wartości bitów (0 i 1).
    runs = {length: {0: 0, 1: 0} for length in range(1, 7)}
    current_bit = bits[0]  # Aktualny bit, od którego zaczynamy liczenie serii.
    length = 1  # Długość bieżącej serii
    # Iterujemy przez kolejne bity, zaczynając od drugiego elementu.
    for bit in bits[1:]:
        if bit == current_bit:
            # Jeśli kolejny bit jest taki sam, zwiększamy długość bieżącej serii.
            length += 1
        else:
            # Jeśli seria się przerwała, ograniczamy długość do maksymalnie 6 (zgodnie z testem).
            if length > 6:
                length = 6
            # Zapisujemy długość serii dla danego bitu.
            runs[length][current_bit] += 1
            # Resetujemy bieżący bit i długość serii.
            current_bit = bit
            length = 1
    # Po zakończeniu pętli obsługujemy ostatnią serię.
    if length > 6:
        length = 6
    runs[length][current_bit] += 1

    # Zdefiniowane przedziały liczebności serii dla długości 1-6,
    # które są uznawane za poprawne dla idealnego ciągu losowego.
    valid_ranges = {
        1: (2315, 2685),
        2: (1114, 1386),
        3: (527, 723),
        4: (240, 384),
        5: (103, 209),
        6: (103, 209)
    }
    # Sprawdzamy, czy liczba wystąpień serii dla obu bitów (0 i 1) mieści się w zadanych przedziałach.
    for length in range(1, 7):
        for bit in (0, 1):
            count = runs[length][bit]
            min_val, max_val = valid_ranges[length]
            if not (min_val <= count <= max_val):
                return False  # Jeśli choć jeden wynik nie mieści się w przedziale, test nie przechodzi.
    return True

# Funkcja long_runs_test(bits) sprawdza, czy w ciągu nie występuje seria (ciąg identycznych bitów) o długości 26 lub więcej.
def long_runs_test(bits):
    current_bit = bits[0]  # Bieżący bit.
    length = 1  # Długość bieżącej serii.
    # Przeglądamy kolejne bity w ciągu.
    for bit in bits[1:]:
        # Jeśli bieżąca seria osiągnie lub przekroczy 26, test nie przechodzi.
        if length >= 26:
            return False
        if bit == current_bit:
            # Jeśli bit jest taki sam, zwiększamy długość serii.
            length += 1
        else:
            # W przypadku zmiany bitu, resetujemy długość serii do 1.
            length = 1
        current_bit = bit
    # Po przejściu całego ciągu upewniamy się, że ostatnia seria nie była zbyt długa.
    return length < 26

# Funkcja poker_test(bits) realizuje pokerowy test losowości,
# dzieląc ciąg bitów na bloki 4-bitowe i analizując ich występowanie.
def poker_test(bits):
    blocks = []
    # Dzielimy ciąg bitów na bloki o długości 4 bitów.
    for i in range(0, len(bits), 4):
        # Łączymy 4 kolejne bity w jeden blok reprezentowany jako ciąg znaków.
        block = "".join(str(bit) for bit in bits[i:i+4])
        blocks.append(block)
    # Zliczamy wystąpienia poszczególnych bloków.
    counts = Counter(blocks)
    # Obliczamy statystykę x zgodnie z definicją testu pokerowego.
    x = (16 / 5000) * sum(v ** 2 for v in counts.values()) - 5000
    # Test przechodzi, jeżeli x mieści się w przedziale [2.16, 46.17].
    return 2.16 <= x <= 46.17

if __name__ == "__main__":
    # Ustalamy długość bitów (choć zmienna bit_length nie jest bezpośrednio używana dalej)
    bit_length = 16
    # Generujemy dwie liczby pierwsze p i q spełniające warunek p % 4 == 3.
    p = generate_prime()
    q = generate_prime()
    print("p:", p)
    print("q:", q)
    # Obliczamy moduł n jako iloczyn dwóch liczb pierwszych.
    n = p * q

    # Generujemy 20000 bitów przy użyciu generatora BBS.
    random_bits = bbs_generator(n, 20000)
    print("Wygenerowany ciąg bitów:", random_bits)
    # Wykonujemy poszczególne testy statystyczne na wygenerowanym ciągu bitów:
    print("Test pojedynczych bitów:", single_bits_test(random_bits))
    print("Test serii:", runs_test(random_bits))
    print("Test długiej serii:", long_runs_test(random_bits))
    print("Test pokerowy:", poker_test(random_bits))
