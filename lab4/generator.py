# generator.py

from pathlib import Path
import secrets
import string

def generate_text(size):
    alphabet = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(secrets.choice(alphabet) for _ in range(1024*1024*size))

def save_file(content, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_files():
    files = {
        "small.txt": 1,
        "medium.txt": 10,
        "large.txt": 50,
    }

    current_dir = Path(__file__).parent
    for filename, size in files.items():
        file_path = current_dir / filename
        print(f"Generowanie pliku {filename} ({size} MB)")
        content = generate_text(size)
        save_file(content, file_path)

    print("Wszystkie pliki testowe zostały wygenerowane i zapisane.")

if __name__ == "__main__":
    generate_files()