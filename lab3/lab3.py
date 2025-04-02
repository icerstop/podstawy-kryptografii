import hashlib
import time
import random
import string
import binascii

def calculate_hashes(text):
    """Generuje i wyświetla wartości skrótu dla podanego tekstu."""
    # Konwersja tekstu na bajty
    text_bytes = text.encode('utf-8')
    
    # Reprezentacja binarna
    binary_parts = []
    for char in text:
        char_code = ord(char)
        if char_code < 128:
            binary_parts.append(format(char_code, '07b'))
        else:
            char_bytes = char.encode('utf-8')
            binary_parts.extend(format(byte, '08b') for byte in char_bytes)
    binary_representation = ' '.join(binary_parts)
    print(f"Binarnie: {binary_representation}")
    
    # Skróty
    md5_hash = hashlib.md5(text_bytes).hexdigest()
    print(f"MD5: {md5_hash}")
    print(f"SHA-1: {hashlib.sha1(text_bytes).hexdigest()}")
    print(f"SHA-224: {hashlib.sha224(text_bytes).hexdigest()}")
    print(f"SHA-256: {hashlib.sha256(text_bytes).hexdigest()}")
    print(f"SHA-384: {hashlib.sha384(text_bytes).hexdigest()}")
    print(f"SHA-512: {hashlib.sha512(text_bytes).hexdigest()}")
    print(f"SHA3-224: {hashlib.sha3_224(text_bytes).hexdigest()}")
    print(f"SHA3-256: {hashlib.sha3_256(text_bytes).hexdigest()}")
    print(f"SHA3-384: {hashlib.sha3_384(text_bytes).hexdigest()}")
    print(f"SHA3-512: {hashlib.sha3_512(text_bytes).hexdigest()}")
    
    return md5_hash

def generate_data(size):
    """Generuje losowy ciąg znaków o zadanej długości"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(size))

def test_hash_function(hash_func, data):
    """Testuje szybkość działania funkcji skrótu i zwraca czas oraz długość skrótu"""
    start_time = time.time()
    hash_obj = hash_func(data.encode('utf-8'))
    hash_value = hash_obj.hexdigest()
    end_time = time.time()
    
    execution_time = (end_time - start_time) * 1000  # w milisekundach
    hash_length = len(hash_value) * 4  # długość w bitach (każdy znak hex to 4 bity)
    
    return execution_time, hash_length, hash_value

def compare_hash_functions():
    """Porównuje szybkość działania i długość wyjścia różnych funkcji skrótu"""
    # Funkcje skrótu do testowania
    hash_functions = {
        "MD5": hashlib.md5,
        "SHA-1": hashlib.sha1,
        "SHA-224": hashlib.sha224,
        "SHA-256": hashlib.sha256,
        "SHA-384": hashlib.sha384,
        "SHA-512": hashlib.sha512,
        "SHA3-224": hashlib.sha3_224,
        "SHA3-256": hashlib.sha3_256,
        "SHA3-384": hashlib.sha3_384,
        "SHA3-512": hashlib.sha3_512
    }
    
    # Różne rozmiary danych do testowania
    data_sizes = [10, 100, 1000, 10000, 100000]
    
    print("\nPorównanie funkcji skrótu:")
    print("-" * 80)
    print(f"{'Funkcja':<10} | {'Rozmiar danych':<15} | {'Czas [ms]':<12} | {'Długość [bit]':<12} | {'Przykład':<20}")
    print("-" * 80)
    
    for size in data_sizes:
        # Generujemy dane testowe o określonym rozmiarze
        test_data = generate_data(size)
        
        for func_name, func in hash_functions.items():
            # Testujemy każdą funkcję
            time_ms, hash_length, hash_value = test_hash_function(func, test_data)
            
            # Wyświetlamy wyniki
            print(f"{func_name:<10} | {size:<15} | {time_ms:.6f}ms | {hash_length:<12} | {hash_value[:20]}...")

def check_common_password(password, md5_hash):
    """Sprawdza czy hasło jest powszechnie znane"""
    # Utworzenie słownika popularnych krótkich haseł (do 4 znaków)
    common_passwords = {
        "": "d41d8cd98f00b204e9800998ecf8427e",
        "a": "0cc175b9c0f1b6a831c399e269772661",
        "ab": "187ef4436122d1cc2f40dc2b92f0eba0",
        "abc": "900150983cd24fb0d6963f7d28e17f72",
        "abcd": "e2fc714c4727ee9395f324cd2e7f331f",
        "1": "c4ca4238a0b923820dcc509a6f75849b",
        "12": "c20ad4d76fe97759aa27a0c99bff6710",
        "123": "202cb962ac59075b964b07152d234b70",
        "1234": "81dc9bdb52d04dc20036dbd8313ed055",
        "pass": "1a1dc91c907325c69271ddf0c944bc72",
        "pass1": "7c6a180b36896a0a8c02787eeafb0e4c",
        "test": "098f6bcd4621d373cade4e832627b4f6",
        "admin": "21232f297a57a5a743894a0e4a801fc3",
        "root": "63a9f0ea7bb98050796b649e85481845",
        "qwer": "962012d09b8170d912f0669f6d7d9d07",
        "asdf": "912ec803b2ce49e4a541068d495ab570",
        "zxcv": "9df62e693988eb4e1e1444ece0578579",
        "aaa": "47bce5c74f589f4867dbd57e9ca9f808",
        "111": "698d51a19d8a121ce581499d7b701668",
        "0000": "4a7d1ed414474e4033ac29ccb8653d9b"
    }
    
    # Sprawdzenie, czy hasło jest w słowniku lub jego skrót jest znany
    if password in common_passwords:
        return True, "Hasło znajduje się w słowniku popularnych haseł"
    
    if md5_hash in common_passwords.values():
        return True, "Skrót MD5 znajduje się w bazie znanych skrótów"
    
    # Symulacja sprawdzenia w większej bazie (dla celów edukacyjnych)
    if len(password) <= 2:
        return True, "Bardzo krótkie hasło (1-2 znaki) jest łatwe do złamania metodą brute-force"
    elif len(password) <= 4:
        return True, "Krótkie hasło (3-4 znaki) jest narażone na atak słownikowy lub rainbow tables"
    
    return False, "Hasło nie zostało znalezione w podstawowej bazie, ale może być narażone na inne ataki"

def discuss_password_security():
    """Omawia bezpieczeństwo krótkich haseł składowanych w bazach danych"""
    print("\nBezpieczeństwo krótkich haseł w bazach danych:")
    print("-" * 80)
    print("1. Krótkie hasła (1-4 znaki) są bardzo podatne na ataki:")
    print("   - Atak brute-force (przeszukanie wszystkich możliwości) jest bardzo szybki")
    print("   - Dla hasła 4-znakowego z małych liter i cyfr mamy tylko 36^4 = 1,6 mln kombinacji")
    print("   - Współczesny komputer może sprawdzić miliony skrótów MD5 na sekundę")
    print("\n2. Rainbow tables:")
    print("   - Są to prekomputowane tabele skrótów dla typowych haseł")
    print("   - Pozwalają na szybkie odwrócenie funkcji skrótu")
    print("   - Dla MD5 istnieją ogromne bazy rainbow tables dostępne publicznie")
    print("\n3. Zalecenia bezpieczeństwa:")
    print("   - Używaj solenia haseł (dodawanie losowego ciągu przed skrótem)")
    print("   - Stosuj wolniejsze funkcje skrótu zaprojektowane do haseł (bcrypt, Argon2)")
    print("   - Wymuś minimalne długości haseł (min. 8-12 znaków)")
    print("   - Implementuj weryfikację dwuskładnikową")

def discuss_md5_security():
    """Omawia bezpieczeństwo funkcji MD5 i znane kolizje"""
    print("\nCzy MD5 jest bezpieczną funkcją skrótu?")
    print("-" * 80)
    print("MD5 NIE jest uznawane za bezpieczną funkcję skrótu w obecnych zastosowaniach kryptograficznych.")
    print("\nZnane kolizje i problemy z MD5:")
    print("1. Historia podatności:")
    print("   - 1996: Hans Dobbertin pokazał pierwsze praktyczne słabości w MD5")
    print("   - 2004: Chińscy badacze (Xiaoyun Wang i Hongbo Yu) opublikowali metodę generowania kolizji")
    print("   - 2005: Arjen Lenstra zademonstrował dwa różne pliki X.509 mające identyczny skrót MD5")
    print("   - 2008: Zespół badaczy (Marc Stevens i inni) stworzył fałszywy certyfikat CA")
    print("   - 2012: Wirus Flame wykorzystał kolizje MD5 do podszywania się pod certyfikat Microsoftu")
    
    print("\n2. Przykładowa znana kolizja:")
    print("   Te dwa ciągi szesnastkowe mają identyczny skrót MD5:")
    print("   d131dd02c5e6eec4... i d131dd02c5e6eec4...")
    print("   Obie wartości mają skrót MD5: 79054025255fb1a26e4bc422aef54eb4")
    
    print("\n3. Problemy z MD5:")
    print("   - Podatność na ataki kolizyjne (znalezienie dwóch wiadomości o tym samym skrócie)")
    print("   - Za krótka długość wyjściowa (128 bitów)")
    print("   - Podatność na ataki preimage w niektórych przypadkach")
    
    print("\n4. Zalecenia:")
    print("   - Nie używać MD5 do nowych zastosowań kryptograficznych")
    print("   - Zastąpić MD5 nowszymi funkcjami jak SHA-256, SHA-3 lub Blake2")
    print("   - Używać SHA-3 lub Blake2 do najbardziej wrażliwych zastosowań")

def find_hash_collisions():
    """Znajduje kolizje dla pierwszych 12 bitów skrótu SHA-256"""
    print("\nBadanie kolizji na pierwszych 12 bitach skrótu SHA-256:")
    print("-" * 80)
    
    # Słownik do przechowywania wartości skrótów (pierwsze 12 bitów jako klucz)
    hash_values = {}
    
    # Licznik prób
    attempts = 0
    
    # Licznik znalezionych kolizji
    collisions = 0
    
    # Maksymalna liczba kolizji do znalezienia
    max_collisions = 5
    
    print("Szukam kolizji...")
    
    while collisions < max_collisions and attempts < 10000:
        attempts += 1
        
        # Generujemy losowy ciąg znaków
        data = generate_data(20)  # 20 znaków
        
        # Obliczamy skrót SHA-256
        hash_value = hashlib.sha256(data.encode('utf-8')).hexdigest()
        
        # Konwertujemy pierwsze 3 znaki hex (12 bitów) na liczbę
        first_12_bits = hash_value[:3]
        
        # Sprawdzamy, czy mamy już taki skrót w słowniku
        if first_12_bits in hash_values:
            collisions += 1
            original_data = hash_values[first_12_bits]
            
            # Wyświetlamy znalezioną kolizję
            print(f"\nKolizja #{collisions} znaleziona po {attempts} próbach:")
            print(f"Dane #1: '{original_data}'")
            print(f"Skrót #1: {hashlib.sha256(original_data.encode('utf-8')).hexdigest()}")
            print(f"Dane #2: '{data}'")
            print(f"Skrót #2: {hash_value}")
            print(f"Pierwsze 12 bitów (3 znaki hex): {first_12_bits}")
        else:
            # Zapisujemy wartość w słowniku
            hash_values[first_12_bits] = data
    
    # Statystyki
    unique_prefixes = len(hash_values)
    theoretical_max = 2**12  # 4096
    
    print(f"\nStatystyki eksperymentu:")
    print(f"Liczba prób: {attempts}")
    print(f"Znalezionych kolizji: {collisions}")
    print(f"Unikalnych prefiksów 12-bitowych: {unique_prefixes}")
    print(f"Teoretyczna maksymalna liczba unikalnych prefiksów: {theoretical_max}")
    
    # Omówienie wyniku
    print("\nWnioski:")
    print("1. Kolizje dla krótkich prefiksów (np. 12 bitów) są łatwe do znalezienia")
    print("2. Dla 12 bitów mamy tylko 2^12 = 4096 możliwych wartości")
    print("3. Według paradoksu urodzin, szansa na kolizję przekracza 50% już przy około 64 próbach (2^(12/2))")
    print("4. Dlatego pełny skrót kryptograficzny musi mieć dużą długość (np. 256 bitów)")
    print("5. To pokazuje, dlaczego krótkie skróty nie są bezpieczne kryptograficznie")

def test_sac_criteria():
    """Testuje kryterium SAC (Strict Avalanche Criteria) dla SHA-256"""
    print("\nBadanie kryterium SAC dla SHA-256:")
    print("-" * 80)
    print("Kryterium SAC: przy zmianie pojedynczego bitu na wejściu, każdy bit wyjściowy")
    print("powinien zmienić się z prawdopodobieństwem 0,5.")
    
    # Wybieramy SHA-256 do testów
    hash_func = hashlib.sha256
    
    # Liczba testów
    num_tests = 10
    
    # Rozmiar danych wejściowych (w bajtach)
    input_size = 16  # 16 bajtów = 128 bitów
    
    # Rozmiar wyjścia SHA-256 (w bitach)
    output_size = 256
    
    # Tablica do zliczania zmian dla każdego bitu wyjściowego
    bit_changes = [0] * output_size
    
    # Liczba wszystkich zmian bitów
    total_bit_flips = 0
    
    # Liczba wszystkich testowanych bitów
    total_bits_tested = 0
    
    print("\nTestuję wpływ zmiany pojedynczego bitu wejściowego na wyjście...")
    
    for test in range(num_tests):
        # Generujemy losowe dane wejściowe
        random_bytes = bytearray(random.getrandbits(8) for _ in range(input_size))
        input_data = bytes(random_bytes)
        
        # Obliczamy oryginalny skrót
        original_hash = hash_func(input_data).digest()
        
        # Konwertujemy skrót na reprezentację binarną (ciąg 0 i 1)
        original_bits = ''.join(format(byte, '08b') for byte in original_hash)
        
        # Dla każdego bitu w danych wejściowych
        for byte_idx in range(len(random_bytes)):
            for bit_idx in range(8):
                # Zmieniamy pojedynczy bit
                modified_bytes = bytearray(input_data)
                modified_bytes[byte_idx] ^= (1 << bit_idx)  # XOR z odpowiednią maską bitową
                
                # Obliczamy nowy skrót
                modified_hash = hash_func(bytes(modified_bytes)).digest()
                
                # Konwertujemy nowy skrót na bity
                modified_bits = ''.join(format(byte, '08b') for byte in modified_hash)
                
                # Liczymy różnice bitów
                for i in range(output_size):
                    if original_bits[i] != modified_bits[i]:
                        bit_changes[i] += 1
                        total_bit_flips += 1
                
                total_bits_tested += 1
    
    # Obliczamy prawdopodobieństwo zmiany dla każdego bitu
    change_probabilities = [changes / total_bits_tested for changes in bit_changes]
    
    # Obliczamy średnie prawdopodobieństwo zmiany
    avg_probability = total_bit_flips / (total_bits_tested * output_size)
    
    # Wyświetlamy wyniki
    print(f"\nWyniki dla {num_tests} losowych danych wejściowych, testując wszystkie możliwe zmiany pojedynczego bitu:")
    print(f"Średnie prawdopodobieństwo zmiany bitu wyjściowego: {avg_probability:.4f}")
    print(f"Idealne prawdopodobieństwo (SAC): 0.5000")
    print(f"Odchylenie od ideału: {abs(avg_probability - 0.5):.4f}")
    
    # Histogram prawdopodobieństw (prosty tekstowy)
    min_prob = min(change_probabilities)
    max_prob = max(change_probabilities)
    
    print(f"\nRozkład prawdopodobieństw zmiany dla poszczególnych bitów wyjściowych:")
    print(f"Minimum: {min_prob:.4f}, Maksimum: {max_prob:.4f}")
    
    # Histogram w formie tekstowej
    histogram = [0] * 10
    for prob in change_probabilities:
        bin_idx = min(9, int(prob * 10))
        histogram[bin_idx] += 1
    
    print("\nHistogram prawdopodobieństw zmiany bitów (0.0-1.0):")
    for i in range(10):
        lower = i / 10
        upper = (i + 1) / 10
        count = histogram[i]
        bar = '#' * (count // 5 + 1)
        print(f"{lower:.1f}-{upper:.1f}: {bar} ({count})")
    
    # Wnioski
    print("\nWnioski:")
    print("1. Dobre funkcje skrótu (jak SHA-256) powinny spełniać kryterium SAC")
    print("2. Idealne prawdopodobieństwo zmiany każdego bitu to 0.5 (50%)")
    print("3. Odchylenia od 0.5 mogą wskazywać na słabości funkcji skrótu")
    print("4. Im bliżej 0.5, tym lepiej funkcja rozprasza zmiany w danych wejściowych")
    print("5. Ta właściwość jest kluczowa dla odporności na kryptoanalizę różnicową")

def main():
    # 1. Najpierw generujemy skróty dla tekstu wprowadzonego przez użytkownika
    text = input("Wprowadź tekst do wygenerowania skrótów: ")
    print("\nWyniki dla wprowadzonego tekstu:")
    md5_hash = calculate_hashes(text)
    
    # 2. Następnie automatycznie porównujemy funkcje skrótu
    compare_hash_functions()
    
    # 3. Sprawdzamy bezpieczeństwo krótkiego hasła
    print("\nTest bezpieczeństwa hasła:")
    print("-" * 80)
    short_password = input("Wprowadź krótkie hasło (max 4 znaki): ")
    
    if len(short_password) > 4:
        print("Wprowadzone hasło jest dłuższe niż 4 znaki, obcinamy do pierwszych 4...")
        short_password = short_password[:4]
        
    print(f"Sprawdzanie bezpieczeństwa hasła: '{short_password}'")
    short_pw_md5 = hashlib.md5(short_password.encode('utf-8')).hexdigest()
    print(f"MD5: {short_pw_md5}")
    
    is_common, message = check_common_password(short_password, short_pw_md5)
    if is_common:
        print(f"UWAGA: {message}")
    else:
        print(message)
    
    # Omówienie bezpieczeństwa krótkich haseł
    discuss_password_security()
    
    # 4. Omówienie bezpieczeństwa MD5 i znanych kolizji
    discuss_md5_security()
    
    # 5. Badanie kolizji na pierwszych 12 bitach skrótu SHA-256
    find_hash_collisions()
    
    # 6. Badanie kryterium SAC dla SHA-256
    test_sac_criteria()

if __name__ == "__main__":
    main()
