#include <bits/stdc++.h>
using namespace std;

/**
 * Sprawdza, czy liczba n jest prawdopodobnie pierwsza
 * (prosty test Miller-Rabin dla kilku podstaw).
 */
bool isProbablyPrime(uint64_t n, int k = 5) {
    if (n < 2) return false;
    if (n % 2 == 0 && n != 2) return false;

    // Funkcja pomocnicza do szybkiego potęgowania modulo
    auto powerMod = [&](uint64_t base, uint64_t exp, uint64_t mod) {
        __uint128_t result = 1;
        __uint128_t b = base % mod;
        while (exp > 0) {
            if (exp & 1) result = (result * b) % mod;
            b = (b * b) % mod;
            exp >>= 1;
        }
        return (uint64_t)result;
    };

    // Rozkład n-1 na d*2^r
    uint64_t d = n - 1;
    int r = 0;
    while ((d & 1) == 0) {
        d >>= 1;
        r++;
    }

    // Test Miller-Rabin
    auto check = [&](uint64_t a) {
        uint64_t x = powerMod(a, d, n);
        if (x == 1 || x == n - 1) return true;
        for (int i = 1; i < r; i++) {
            x = (__uint128_t)x * x % n;
            if (x == n - 1) return true;
        }
        return false;
    };

    // Kilka losowych baz (lub stałych) do testu
    static vector<uint64_t> testPrimes = {2, 3, 5, 7, 11, 13, 17, 19, 23};
    for (int i = 0; i < k; i++) {
        uint64_t a;
        if (i < (int)testPrimes.size()) {
            a = testPrimes[i];
        } else {
            // Losowa podstawa
            a = 2 + rand() % (n - 3);
        }
        if (a == 0 || a == 1 || a == n) continue;
        if (!check(a)) return false;
    }
    return true;
}

/**
 * Funkcja zwraca losową liczbę (64-bit), która spełnia warunek:
 *   1) Jest prawdopodobnie pierwsza.
 *   2) p ≡ 3 (mod 4).
 *   3) Ma zadany przybliżony rozmiar bitowy (bitLength).
 *
 * UWAGA: Dla poważnych zastosowań kryptograficznych
 *        warto skorzystać z profesjonalnych bibliotek.
 */
uint64_t generatePrime3Mod4(int bitLength) {
    static random_device rd;
    static mt19937_64 gen(rd());

    uniform_int_distribution<uint64_t> dist(0ULL, (1ULL << bitLength) - 1);

    while (true) {
        uint64_t candidate = dist(gen);

        // Upewnijmy się, że najwyższy bit jest ustawiony, aby zachować bitLength
        candidate |= (1ULL << (bitLength - 1));
        // Wymuś kandydata w formie 3 (mod 4)
        if (candidate % 4 != 3) {
            candidate -= (candidate % 4);
            candidate += 3;
        }
        if (isProbablyPrime(candidate)) {
            return candidate;
        }
    }
}

/**
 * Oblicza N = p * q, gdzie p i q to duże liczby pierwsze (p ≡ q ≡ 3 mod 4).
 * Tutaj generujemy je losowo o rozmiarze bitLength (dla uproszczenia tak samo).
 */
uint64_t generateN(int bitLength) {
    uint64_t p = generatePrime3Mod4(bitLength);
    uint64_t q = generatePrime3Mod4(bitLength);

    // Żeby uniknąć sytuacji p == q, w razie potrzeby powtarzamy
    while (p == q) {
        q = generatePrime3Mod4(bitLength);
    }

    return p * q;
}

/**
 * Oblicza NWD (algorytm Euklidesa) - potrzebne do upewnienia się, że x0 i N są względnie pierwsze.
 */
uint64_t gcd64(uint64_t a, uint64_t b) {
    while (b != 0) {
        uint64_t t = b;
        b = a % b;
        a = t;
    }
    return a;
}

/**
 * Generuje losowe x0 takie, że NWD(x0, N) = 1.
 */
uint64_t generateX0(uint64_t N) {
    static random_device rd;
    static mt19937_64 gen(rd());
    uniform_int_distribution<uint64_t> dist(2, N-2);

    while (true) {
        uint64_t candidate = dist(gen);
        if (gcd64(candidate, N) == 1) {
            return candidate;
        }
    }
}

/**
 * Klasa BlumBlumShub do generowania bitów.
 */
class BlumBlumShub {
private:
    uint64_t N;    // Iloczyn p*q
    uint64_t state; // Bieżący stan generatora x_n

public:
    BlumBlumShub(uint64_t N_, uint64_t seed) : N(N_), state(seed) {}

    // Zwraca kolejny bit pseudolosowy (LSB z x_n).
    int getNextBit() {
        // x_{n+1} = (x_n)^2 mod N
        state = ( (__uint128_t)state * state ) % N;
        // Bit wyjściowy to najmłodszy bit state
        return (int)(state & 1ULL);
    }

    // Generuje ciąg length bitów i zwraca w postaci stringa lub wektora.
    string getBitSequence(size_t length) {
        ostringstream oss;
        for (size_t i = 0; i < length; i++) {
            oss << getNextBit();
        }
        return oss.str();
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    // 1) Wybieramy rozmiar bitowy liczb p i q (dla demonstracji 16, co jest MALUTKIE w praktyce)
    int bitLength = 16;
    cout << "Generowanie N (p*q) o rozmiarze ~" << bitLength << " bitów...\n";
    uint64_t N = generateN(bitLength);
    cout << "N = " << N << "\n";

    // 2) Generujemy x0
    uint64_t x0 = generateX0(N);
    cout << "x0 = " << x0 << "\n";

    // 3) Tworzymy obiekt generatora BlumBlumShub
    BlumBlumShub bbs(N, x0);

    // 4) Generujemy przykładowy ciąg bitów
    size_t numBits = 1000; // Dla przykładu
    cout << "Generowanie " << numBits << " bitów...\n";
    string bitSequence = bbs.getBitSequence(numBits);

    // 5) Prosty test: zliczanie ile jest jedynek i zer
    size_t countOnes = 0, countZeros = 0;
    for (char c : bitSequence) {
        if (c == '1') countOnes++;
        else countZeros++;
    }

    cout << "Wygenerowany ciąg (pierwsze 64 bity):\n";
    cout << bitSequence.substr(0, 64) << (bitSequence.size() > 64 ? "..." : "") << "\n\n";
    cout << "Liczba bitów = " << bitSequence.size() << "\n";
    cout << "Liczba jedynek = " << countOnes << "\n";
    cout << "Liczba zer    = " << countZeros << "\n";

    // 6) Minimalna analiza statystyczna:
    double ratio = (double)countOnes / (double)bitSequence.size();
    cout << fixed << setprecision(4);
    cout << "Proporcja jedynek: " << (ratio * 100.0) << "%\n";
    if (ratio > 0.45 && ratio < 0.55) {
        cout << "W miare OK – wygląda na w miarę zrównoważony ciąg.\n";
    } else {
        cout << "Uwaga! Rozklad bitow (0/1) nie jest rownomierny w prostym tescie.\n";
    }

    cout << "\n--- Koniec demonstracji Blum-Blum-Shub ---\n";
    cout << "PS. W prawdziwych zastosowaniach wybierz duuuużo większe p i q!\n";

    return 0;
}
