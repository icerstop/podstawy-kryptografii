# plot_results.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def add_labels(ax, precision=2):
    format_string = f'%.{precision}f'
    for container in ax.containers:
        ax.bar_label(container, fmt=format_string, label_type='edge', padding=3)


def plot_times():
    df = pd.read_csv("results.csv")

    plt.figure()
    for mode in df['Mode'].unique():
        mode_data = df[df['Mode'] == mode]
        plt.plot(mode_data['File'], mode_data['Encryption Time (s)'], marker='o', label=mode)

    plt.title("Czas szyfrowania AES w różnych trybach")
    plt.xlabel("Plik testowy")
    plt.ylabel("Czas szyfrowania (s)")
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("encryption_times.png")
    print("Wykres czasu szyfrowania zapisany jako encryption_times.png")

    plt.figure()
    for mode in df['Mode'].unique():
        mode_data = df[df['Mode'] == mode]
        plt.plot(mode_data['File'], mode_data['Decryption Time (s)'], marker='o', label=mode)

    plt.title("Czas deszyfrowania AES w różnych trybach")
    plt.xlabel("Plik testowy")
    plt.ylabel("Czas deszyfrowania (s)")
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("decryption_times.png")
    print("Wykres czasu deszyfrowania zapisany jako decryption_times.png")


def plot_times_library_only():
    df = pd.read_csv("results.csv")
    df_library = df[df['Mode'].isin(['ECBMode', 'CBCMode', 'CTRMode'])]

    plt.figure()
    for mode in df_library['Mode'].unique():
        mode_data = df_library[df_library['Mode'] == mode]
        plt.plot(mode_data['File'], mode_data['Encryption Time (s)'], marker='o', label=mode)

    plt.title("Czas szyfrowania AES (biblioteka)")
    plt.xlabel("Plik testowy")
    plt.ylabel("Czas szyfrowania (s)")
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("encryption_times_library.png")
    print("Wykres czasu szyfrowania zapisany jako encryption_times_library.png")

    plt.figure()
    for mode in df_library['Mode'].unique():
        mode_data = df_library[df_library['Mode'] == mode]
        plt.plot(mode_data['File'], mode_data['Decryption Time (s)'], marker='o', label=mode)

    plt.title("Czas deszyfrowania AES (biblioteka)")
    plt.xlabel("Plik testowy")
    plt.ylabel("Czas deszyfrowania (s)")
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("decryption_times_library.png")
    print("Wykres czasu deszyfrowania zapisany jako decryption_times_library.png")


def plot_error_propagation():
    df = pd.read_csv("results_errors.csv")

    labels = df['File'].unique()
    modes = df['Mode'].unique()
    x = range(len(labels))
    width = 0.2

    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    for idx, mode in enumerate(modes):
        mode_data = df[df['Mode'] == mode]
        ax.bar(
            [pos + width * idx for pos in x],
            mode_data['Input Diff'],
            width=width,
            label=mode
        )

    add_labels(ax, precision=2)
    plt.title("Propagacja błędów (zmiana bitu w wejściu)")
    plt.xlabel("Plik testowy")
    plt.ylabel("Liczba zmienionych bajtów w szyfrogramie")
    plt.xticks([pos + width * len(modes) / 2 for pos in x], labels)
    plt.legend()
    plt.tight_layout()
    plt.grid(axis='y')
    formatter = mticker.FuncFormatter(lambda x, pos: f"{x/1e6:.1f} × 10^6")
    ax.yaxis.set_major_formatter(formatter)
    plt.savefig("error_propagation_input.png")
    print("Wykres propagacji błędów (zmiana bitu w wejściu) zapisany jako error_propagation_input.png")

    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    for idx, mode in enumerate(modes):
        mode_data = df[df['Mode'] == mode]
        ax.bar(
            [pos + width * idx for pos in x],
            mode_data['Cipher Diff'],
            width=width,
            label=mode
        )

    add_labels(ax, precision=2)
    plt.title("Propagacja błędów (zmiana bitu w szyfrogramie)")
    plt.xlabel("Plik testowy")
    plt.ylabel("Liczba zmienionych bajtów w szyfrogramie")
    plt.xticks([pos + width * len(modes) / 2 for pos in x], labels)
    plt.legend()
    plt.tight_layout()
    plt.grid(axis='y')
    formatter = mticker.FuncFormatter(lambda x, pos: f"{x/1e6:.1f} × 10^6")
    ax.yaxis.set_major_formatter(formatter)
    plt.savefig("error_propagation_cipher.png")
    print("Wykres propagacji błędów (zmiana bitu w szyfrogramie) zapisany jako error_propagation_cipher.png")


def plot_error_propagation_per_file():
    df = pd.read_csv("results_errors.csv")
    modes = df['Mode'].unique()

    file_sizes = {
        'small.txt': 1 * 1024 * 1024,
        'medium.txt': 10 * 1024 * 1024,
        'large.txt': 50 * 1024 * 1024
    }

    for file_name in df['File'].unique():
        file_data = df[df['File'] == file_name]
        file_size = file_sizes[file_name]

        # Input Diff - liczby
        plt.figure(figsize=(8, 5))
        ax = plt.gca()
        ax.bar(file_data['Mode'], file_data['Input Diff'], color='skyblue')
        add_labels(ax, precision=2)
        plt.title(f"Propagacja błędów w wiadomości - {file_name}")
        plt.xlabel("Tryb szyfrowania")
        plt.ylabel("Liczba zmienionych bajtów w szyfrogramie")
        plt.yscale('log')
        plt.grid(axis='y')
        plt.tight_layout()
        plt.savefig(f"error_input_{file_name}.png")
        print(f"Wykres propagacji błędów w wiadomości zapisany jako error_input_{file_name}.png")

        # Cipher Diff - liczby
        plt.figure(figsize=(8, 5))
        ax = plt.gca()
        ax.bar(file_data['Mode'], file_data['Cipher Diff'], color='salmon')
        add_labels(ax, precision=2)
        plt.title(f"Propagacja błędów w szyfrogramie - {file_name}")
        plt.xlabel("Tryb szyfrowania")
        plt.ylabel("Liczba zmienionych bajtów w wiadomości")
        plt.yscale('log')
        plt.grid(axis='y')
        plt.tight_layout()
        plt.savefig(f"error_cipher_{file_name}.png")
        print(f"Wykres propagacji błędów w szyfrogramie zapisany jako error_cipher_{file_name}.png")

        # Input Diff - procenty
        plt.figure(figsize=(8, 5))
        ax = plt.gca()
        percent_input_diff = (file_data['Input Diff'] / file_size) * 100
        ax.bar(file_data['Mode'], percent_input_diff, color='dodgerblue')
        add_labels(ax, precision=6)
        plt.title(f"Procentowa propagacja błędów w wiadomości - {file_name}")
        plt.xlabel("Tryb szyfrowania")
        plt.ylabel("Procent zmienionych bajtów w szyfrogramie (%)")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.savefig(f"percent_error_input_{file_name}.png")
        print(f"Wykres procentowej propagacji błędów w wiadomości zapisany jako percent_error_input_{file_name}.png")

        # Cipher Diff - procenty
        plt.figure(figsize=(8, 5))
        ax = plt.gca()
        percent_cipher_diff = (file_data['Cipher Diff'] / file_size) * 100
        ax.bar(file_data['Mode'], percent_cipher_diff, color='orangered')
        add_labels(ax, precision=6)
        plt.title(f"Procentowa propagacja błędów w szyfrogramie - {file_name}")
        plt.xlabel("Tryb szyfrowania")
        plt.ylabel("Procent zmienionych bajtów w wiadomości (%)")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.savefig(f"percent_error_cipher_{file_name}.png")
        print(f"Wykres procentowej propagacji błędów w szyfrogramie zapisany jako percent_error_cipher_{file_name}.png")

def plot_encryption_decryption_ratio():
    df = pd.read_csv("results.csv")
    df['Ratio'] = df['Encryption Time (s)'] / df['Decryption Time (s)']

    plt.figure(figsize=(10, 6))
    for mode in df['Mode'].unique():
        mode_data = df[df['Mode'] == mode]
        plt.plot(mode_data['File'], mode_data['Ratio'], marker='o', label=mode)

    plt.title("Stosunek czasu szyfrowania do deszyfrowania")
    plt.xlabel("Plik testowy")
    plt.ylabel("Szyfrowanie / Deszyfrowanie")
    plt.axhline(1, color='gray', linestyle='--', linewidth=1)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("encryption_decryption_ratio.png")
    print("Wykres stosunku szyfrowania do deszyfrowania zapisany jako encryption_decryption_ratio.png")

if __name__ == "__main__":
    plot_times()
    plot_times_library_only()
    plot_error_propagation()
    plot_error_propagation_per_file()
    plot_encryption_decryption_ratio()
