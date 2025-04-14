# main.py

from pathlib import Path
from ciphers import ECBMode, CBCMode, CTRMode, ManualCBC
from utils import measure_time, analyze_error_propagation
from generator import generate_files
import csv
from plot_results import plot_times, plot_error_propagation, plot_times_library_only, plot_error_propagation_per_file, plot_encryption_decryption_ratio

results = []
results_errors = []

MODES_TO_TEST = [ECBMode, CBCMode, CTRMode, ManualCBC]

FILES = [
    Path("small.txt"),
    Path("medium.txt"),
    Path("large.txt"),
]

def process_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        

    for mode_class in MODES_TO_TEST:
        cipher = mode_class()
        print(f"\n Tryb: {mode_class.__name__}")

        (encrypted, enc_time) = measure_time(cipher.encrypt)(data)
        print(f"Czas szyfrowania: {enc_time:.6f} sekundy")

        (decrypted, dec_time) = measure_time(cipher.decrypt)(encrypted)
        print(f"Czas deszyfrowania: {dec_time:.6f} sekundy")

        if decrypted != data:
            print("Błąd: Otrzymano inny tekst jawny po deszyfrowaniu.")
        else:
            print("Deszyfrowanie zakończone sukcesem.")
        
        diff_input, diff_cipher = analyze_error_propagation(mode_class, data)

        results.append([file_path.name, mode_class.__name__, enc_time, dec_time])

        results_errors.append([file_path.name, mode_class.__name__, diff_input, diff_cipher])

    

if __name__ == "__main__":
    print("Generowanie plików tekstowych...")
    generate_files()

    for file in FILES:
        print(f"\n=========================")
        print(f"Przetwarzanie pliku: {file.name}")
        print(f"=========================")
        process_file(file)

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["File", "Mode", "Encryption Time (s)", "Decryption Time (s)"])
        writer.writerows(results)
    
    print("Wyniki zostały zapisane do pliku results.csv\n")

    plot_times()
    print("Wykresy czasów encrypt/decrypt zostały wygenerowane i zapisane.\n")

    plot_times_library_only()
    print("Wykresy czasów encrypt/decrypt dla trybów z biblioteki zostały wygenerowane i zapisane.\n")

    with open("results_errors.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["File", "Mode", "Input Diff", "Cipher Diff"])
        writer.writerows(results_errors)

    plot_error_propagation()
    print("Wykresy propagacji błędów zostały wygenerowane i zapisane.\n")

    plot_error_propagation_per_file()
    print("Wykresy propagacji błędów dla każdego pliku zostały wygenerowane i zapisane.\n")

    plot_encryption_decryption_ratio()
    print("Wykresy stosunku szyfrowania do deszyfrowania zostały wygenerowane i zapisane.\n")
    
