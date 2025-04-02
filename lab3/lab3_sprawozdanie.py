import hashlib
import time
import random
import string
import binascii
import secrets
import matplotlib.pyplot as plt
import numpy as np

HASH_FUNCTIONS = [
    'md5',  
    'sha256',
    'sha3_512'
]

SIZES_MB = [10, 25, 50]

def generate_data(size):
    return secrets.token_bytes(size * 1024 * 1024)  # 1MB = 1024*1024 B

def generate_data_str(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def measure_hash_speed(data: bytes):
    results = {}
    for algo in HASH_FUNCTIONS:
        hash_func = getattr(hashlib, algo)
        start = time.perf_counter()
        hash_func(data).digest()
        end = time.perf_counter()
        results[algo] = end - start
    return results

def benchmark_hashing():
    for size in SIZES_MB:
        print(f"\n=== Rozmiar danych: {size} MB ===")
        data = generate_data(size)
        results = measure_hash_speed(data)
        for algo, duration in results.items():
            print(f"{algo.upper():<10}: {duration:.6f} s")
    print('\n')

def flip_bit(data: bytes, bit_index: int) -> bytes:
    byte_index = bit_index // 8
    bit_in_byte = bit_index % 8
    flipped_byte = data[byte_index] ^ (1 << bit_in_byte)  # zmiana bitu za pomocą XOR
    return data[:byte_index] + bytes([flipped_byte]) + data[byte_index + 1:]

def count_bit_differences(a: bytes, b: bytes) -> int:
    return sum(bin(x ^ y).count('1') for x, y in zip(a, b))

# =====================================================================
# Wydzielenie rdzenia obliczeniowego SAC do jednej funkcji compute_sac()
# =====================================================================
def compute_sac(hash_func_name='sha256', input_size=32):
    """
    Oblicza średnią liczbę zmienionych bitów wyjścia (SAC) dla pojedynczego testu.
    Zwraca krotkę: (średnia liczba zmienionych bitów, długość hashu w bitach).
    """
    hash_func = getattr(hashlib, hash_func_name)
    input_bits = input_size * 8
    original_data = secrets.token_bytes(input_size)
    original_hash = hash_func(original_data).digest()
    total_changed_bits = 0

    for i in range(input_bits):
        modified_data = flip_bit(original_data, i)
        modified_hash = hash_func(modified_data).digest()
        total_changed_bits += count_bit_differences(original_hash, modified_hash)
    
    avg_change = total_changed_bits / input_bits
    hash_len_bits = len(original_hash) * 8
    return avg_change, hash_len_bits

def test_sac(hash_func_name='sha256', input_size=32):
    """
    Wykonuje pojedynczy test SAC, korzystając z compute_sac() i drukuje wyniki.
    """
    avg_change, hash_len_bits = compute_sac(hash_func_name, input_size)
    percent = avg_change / hash_len_bits
    print(f"Funkcja skrótu: {hash_func_name.upper()}")
    print(f"Średnia liczba zmienionych bitów wyjścia: {avg_change:.2f} / {hash_len_bits}")
    print(f"Prawdopodobieństwo zmiany pojedynczego bitu wyjściowego: {percent:.3%}")

def collect_sac_stats(hash_func_name='sha256', input_size=32, repetitions=10):
    """
    Powtarza test SAC, korzystając z compute_sac(), i zwraca listę średnich zmian.
    """
    averages = []
    for rep in range(repetitions):
        avg_change, _ = compute_sac(hash_func_name, input_size)
        averages.append(avg_change)
    return averages

def get_hash_bits(hash_bytes: bytes, n_bits: int) -> str:
    return ''.join(f'{byte:08b}' for byte in hash_bytes)[:n_bits]

def test_prefix_collisions(hash_func_name='md5', input_size=32, num_trials=1000, bit_length=[12, 24, 48]):
    hash_func = getattr(hashlib, hash_func_name)
    m = secrets.token_bytes(input_size)
    h_m = hash_func(m).digest()

    collisions = {n: 0 for n in bit_length}
    prefixes_8 = set()

    for i in range(num_trials):
        m_prime = secrets.token_bytes(input_size)
        h_m_prime = hash_func(m_prime).digest()
        prefixes_8.add(h_m_prime[0])
        for n in bit_length:
            if hash_prefix_equal(h_m, h_m_prime, n):
                collisions[n] += 1

    print(f"\nUnikalnych 8-bitowych prefiksów: {len(prefixes_8)} z 256 możliwych")
    print(f"Funkcja skrótu: {hash_func_name.upper()} - test kolizji prefiksu dla {num_trials} wiadomości:")
    for n in bit_length:
        expected = num_trials / (2 ** n)
        print(f" - {n} bitów: kolizji = {collisions[n]}, oczekiwane = {expected:.3f}")

def hash_prefix_equal(h1: bytes, h2: bytes, n_bits: int) -> bool:
    """Porównuje n pierwszych bitów dwóch skrótów (binarnie, bez konwersji na string)."""
    byte_count = (n_bits + 7) // 8  # zaokrąglona liczba bajtów
    h1_part = h1[:byte_count]
    h2_part = h2[:byte_count]

    extra_bits = (8 * byte_count) - n_bits
    if extra_bits:
        mask = (0xFF << extra_bits) & 0xFF
        return h1_part[:-1] == h2_part[:-1] and (h1_part[-1] & mask) == (h2_part[-1] & mask)
    else:
        return h1_part == h2_part

# ================================
# Funkcje zbierające statystyki
# ================================
def collect_hash_speed_stats(repetitions=10):
    stats = {}
    for size in SIZES_MB:
        stats[size] = {algo: [] for algo in HASH_FUNCTIONS}
        for rep in range(repetitions):
            data = generate_data(size)
            results = measure_hash_speed(data)
            for algo, duration in results.items():
                stats[size][algo].append(duration)
    return stats

def plot_hash_speed_stats(stats, save_plots=False):
    """
    Generuje wykres słupkowy średnich czasów haszowania z odchyleniem standardowym.
    Jeśli save_plots=True, zapisuje wykresy jako pliki PNG.
    """
    for size, algos in stats.items():
        algorithms = list(algos.keys())
        means = [np.mean(algos[algo]) for algo in algorithms]
        stds = [np.std(algos[algo]) for algo in algorithms]
        
        plt.figure(figsize=(10, 6))
        plt.bar(algorithms, means, yerr=stds, capsize=5)
        plt.title(f"Czas haszowania dla rozmiaru danych {size} MB")
        plt.xlabel("Funkcja skrótu")
        plt.ylabel("Czas (s)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_plots:
            plt.savefig(f"hash_speed_{size}MB.png")
        plt.show()

def plot_sac_stats(averages, hash_func_name='sha256', save_plots=False):
    """
    Wizualizuje wyniki testu SAC – histogram oraz wykres średniej z błędem.
    Jeśli save_plots=True, zapisuje wykresy jako pliki PNG.
    """
    mean_val = np.mean(averages)
    std_val = np.std(averages)
    
    # Histogram
    plt.figure(figsize=(8, 6))
    plt.hist(averages, bins=10, edgecolor='black')
    plt.title(f"Rozkład średniej liczby zmienionych bitów dla {hash_func_name.upper()}")
    plt.xlabel("Średnia liczba zmienionych bitów")
    plt.ylabel("Częstotliwość")
    plt.tight_layout()
    if save_plots:
        plt.savefig(f"sac_histogram_{hash_func_name}.png")
    plt.show()
    
    # Wykres średniej z odchyleniem
    plt.figure(figsize=(6, 4))
    plt.errorbar([0], [mean_val], yerr=[std_val], fmt='o', capsize=10)
    plt.title(f"Średnia zmiana bitów: {mean_val:.2f} ± {std_val:.2f}")
    plt.xticks([])
    plt.ylabel("Średnia liczba zmienionych bitów")
    plt.tight_layout()
    if save_plots:
        plt.savefig(f"sac_errorbar_{hash_func_name}.png")
    plt.show()

def collect_prefix_collision_stats(hash_func_name='sha256', input_size=128, num_trials=100000, bit_length=[8, 16, 24], repetitions=5):
    stats = {n: [] for n in bit_length}
    for rep in range(repetitions):
        hash_func = getattr(hashlib, hash_func_name)
        m = secrets.token_bytes(input_size)
        h_m = hash_func(m).digest()
        collisions = {n: 0 for n in bit_length}
        for i in range(num_trials):
            m_prime = secrets.token_bytes(input_size)
            h_m_prime = hash_func(m_prime).digest()
            for n in bit_length:
                if hash_prefix_equal(h_m, h_m_prime, n):
                    collisions[n] += 1
        for n in bit_length:
            stats[n].append(collisions[n])
    return stats

def plot_prefix_collision_stats(stats, num_trials, bit_length=[8, 16, 24], save_plots=False):
    """
    Generuje wykres słupkowy średniej liczby kolizji dla różnych długości prefiksu z odchyleniem standardowym.
    Jeśli save_plots=True, zapisuje wykres jako plik PNG.
    """
    averages = [np.mean(stats[n]) for n in bit_length]
    stds = [np.std(stats[n]) for n in bit_length]
    expected = [num_trials / (2 ** n) for n in bit_length]
    
    plt.figure(figsize=(10, 6))
    x = np.arange(len(bit_length))
    plt.bar(x, averages, yerr=stds, capsize=5, tick_label=[f"{n} bitów" for n in bit_length])
    plt.plot(x, expected, 'r--', label="Oczekiwane")
    plt.title("Test kolizji prefiksu")
    plt.xlabel("Długość prefiksu")
    plt.ylabel("Liczba kolizji")
    plt.legend()
    plt.tight_layout()
    if save_plots:
        plt.savefig("prefix_collision.png")
    plt.show()

# =====================================
# Dodatkowe statystyki (inne przykłady)
# =====================================
def collect_hash_throughput_stats(algorithm_list=HASH_FUNCTIONS, data_size=50, repetitions=10):
    throughput = {algo: [] for algo in algorithm_list}
    for rep in range(repetitions):
        data = generate_data(data_size)
        for algo in algorithm_list:
            hash_func = getattr(hashlib, algo)
            start = time.perf_counter()
            hash_func(data).digest()
            end = time.perf_counter()
            elapsed = end - start
            throughput[algo].append(data_size / elapsed if elapsed > 0 else 0)
    return throughput

def plot_hash_throughput_stats(throughput_stats, save_plots=False):
    algorithms = list(throughput_stats.keys())
    means = [np.mean(throughput_stats[algo]) for algo in algorithms]
    stds = [np.std(throughput_stats[algo]) for algo in algorithms]
    
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, means, yerr=stds, capsize=5)
    plt.title("Przepustowość funkcji skrótu (MB/s)")
    plt.xlabel("Funkcja skrótu")
    plt.ylabel("Przepustowość (MB/s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save_plots:
        plt.savefig("hash_throughput.png")
    plt.show()

def collect_bit_distribution_stats(input_size=32, repetitions=10):
    stats = {algo: [] for algo in HASH_FUNCTIONS}
    for rep in range(repetitions):
        data = secrets.token_bytes(input_size)
        for algo in HASH_FUNCTIONS:
            hash_func = getattr(hashlib, algo)
            digest = hash_func(data).digest()
            total_bits = len(digest) * 8
            ones = sum(bin(b).count('1') for b in digest)
            percentage = (ones / total_bits) * 100
            stats[algo].append(percentage)
    return stats

def plot_bit_distribution_stats(stats, save_plots=False):
    algorithms = list(stats.keys())
    means = [np.mean(stats[algo]) for algo in algorithms]
    stds = [np.std(stats[algo]) for algo in algorithms]
    
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, means, yerr=stds, capsize=5)
    plt.axhline(50, color='red', linestyle='--', label='50%')
    plt.title("Rozkład procentowy jedynek w haśhu")
    plt.xlabel("Funkcja skrótu")
    plt.ylabel("Procent jedynek (%)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    if save_plots:
        plt.savefig("bit_distribution.png")
    plt.show()

# ================================
# Główna funkcja programu
# ================================
def main():
    # Oryginalne testy
    benchmark_hashing()
    test_sac('sha256')
    test_prefix_collisions('sha256', input_size=128, num_trials=100000, bit_length=[8, 16, 24])
    
    # Statystyki prędkości haszowania
    print("\n=== Statystyki prędkości haszowania ===")
    hash_speed_stats = collect_hash_speed_stats(repetitions=10)
    for size, algos in hash_speed_stats.items():
        print(f"\nRozmiar danych: {size} MB")
        for algo, times in algos.items():
            print(f"  {algo.upper():<10}: {times}")
    plot_hash_speed_stats(hash_speed_stats, save_plots=True)
    
    # Statystyki efektu lawinowego (SAC)
    print("\n=== Statystyki efektu lawinowego (SAC) ===")
    sac_stats = collect_sac_stats('sha256', input_size=32, repetitions=10)
    print("Surowe dane SAC:", sac_stats)
    plot_sac_stats(sac_stats, 'sha256', save_plots=True)
    
    # Statystyki kolizji prefiksu
    print("\n=== Statystyki kolizji prefiksu ===")
    prefix_stats = collect_prefix_collision_stats('sha256', input_size=128, num_trials=100000, bit_length=[8, 16, 24], repetitions=5)
    print("Surowe dane kolizji prefiksu:")
    for n, values in prefix_stats.items():
        print(f"  {n} bitów: {values}")
    plot_prefix_collision_stats(prefix_stats, num_trials=100000, bit_length=[8, 16, 24], save_plots=True)
    
    # Dodatkowe statystyki: Przepustowość funkcji skrótu
    print("\n=== Statystyki przepustowości funkcji skrótu (MB/s) ===")
    throughput_stats = collect_hash_throughput_stats(data_size=50, repetitions=10)
    for algo, values in throughput_stats.items():
        print(f"  {algo.upper():<10}: {values}")
    plot_hash_throughput_stats(throughput_stats, save_plots=True)
    
    # Dodatkowe statystyki: Rozkład bitów w haśhu
    print("\n=== Statystyki rozkładu jedynek w haśhu (%) ===")
    bit_dist_stats = collect_bit_distribution_stats(input_size=32, repetitions=10)
    for algo, values in bit_dist_stats.items():
        print(f"  {algo.upper():<10}: {values}")
    plot_bit_distribution_stats(bit_dist_stats, save_plots=True)

if __name__ == '__main__':
    main()
