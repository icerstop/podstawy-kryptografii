import secrets

class Trivial:
    def __init__(self, k):
        self.k = k
    
    def split(self, secret, n):
        shares = [secrets.randbelow(self.k) for _ in range(n - 1)]
        final_share = (secret - sum(shares)) % self.k
        shares.append(final_share)
        return shares

    def reconstruct(self, shares):
        return sum(shares) % self.k    
    

# ------------------------------------------------------------
# Wyjaśnienie (wady i ograniczenia trywialnej metody dzielenia sekretu):
#
# 1. Bezpieczeństwo:
#    - Metoda jest całkowicie NIEBEZPIECZNA w sensie kryptograficznym.
#    - Znając n-1 udziałów, można łatwo obliczyć brakujący udział i odtworzyć sekret.
#
# 2. Brak niezależności udziałów:
#    - Ostatni udział jest deterministycznie obliczany z pozostałych udziałów i sekretu.
#    - Wystarczy znać wszystkie oprócz jednego udziału, aby poznać sekret.
#
# 3. Brak mechanizmu progowego:
#    - Nie można ustawić progu t < n – do odtworzenia sekretu wymagane są wszystkie udziały.
#
# 4. Małe wartości k:
#    - Dla małych k (np. k = 10), przestrzeń sekretów jest niewielka → łatwe brute-force.
#
# Wniosek:
# Ta metoda może być wykorzystana jedynie do celów edukacyjnych.
# W zastosowaniach praktycznych należy stosować bezpieczne schematy, np. Shamir's Secret Sharing.
# ------------------------------------------------------------