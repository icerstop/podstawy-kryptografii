# utils.py

import time

def measure_time(func):
    
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return result, end - start
    return wrapper

def flip_bit(data: bytes, bit_index: int) -> bytes:
    byte_index = bit_index // 8
    bit_in_byte = bit_index % 8
    modified = bytearray(data)
    modified[byte_index] ^= 1 << bit_in_byte
    return bytes(modified)

def count_differences(data1: bytes, data2: bytes) -> int:
    return sum(b1 != b2 for b1, b2 in zip(data1, data2))

def analyze_error_propagation(cipher_class, data: bytes):
    cipher = cipher_class()
    encrypted = cipher.encrypt(data)

    tampered_plain = flip_bit(data, 0)
    encrypted_tampered = cipher.encrypt(tampered_plain)
    diff_input = count_differences(encrypted, encrypted_tampered)
    print(f'Zmiana bitu w wiadomości -> różnice {diff_input} bajtów')
    
    tampered_cipher = flip_bit(encrypted, 0)
    decrypted_tampered = cipher.decrypt(tampered_cipher)
    diff_cipher = count_differences(data, decrypted_tampered)
    print(f'Zmiana bitu w szyfrogramie -> różnice {diff_cipher} bajtów')

    return diff_input, diff_cipher
    