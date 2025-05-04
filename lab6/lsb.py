from PIL import Image
import argparse


def _int_to_bin(rgb):
    """Convert integer tuple (R, G, B) to tuple of binary strings."""
    return tuple(format(x, '08b') for x in rgb)


def _bin_to_int(rgb_bin):
    """Convert tuple of binary strings to integer tuple (R, G, B)."""
    return tuple(int(b, 2) for b in rgb_bin)


def encode_lsb(input_path, output_path, message):
    """
    Ukrywa wiadomość w obrazie metodą LSB.
    """
    image = Image.open(input_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    pixels = image.load()

    delimiter = '====='
    data = message + delimiter
    binary_data = ''.join(format(ord(ch), '08b') for ch in data)
    data_len = len(binary_data)

    width, height = image.size
    max_capacity = width * height * 3
    if data_len > max_capacity:
        raise ValueError('Wiadomość jest za długa, by zmieścić się w obrazie.')

    idx = 0
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            r_bin, g_bin, b_bin = _int_to_bin((r, g, b))
            new_bins = []
            for bit in (r_bin, g_bin, b_bin):
                if idx < data_len:
                    new_bins.append(bit[:-1] + binary_data[idx])
                    idx += 1
                else:
                    new_bins.append(bit)
            pixels[x, y] = _bin_to_int(tuple(new_bins))
            if idx >= data_len:
                break
        if idx >= data_len:
            break

    image.save(output_path)
    print(f'Zakodowano wiadomość. Plik wyjściowy: {output_path}')


def decode_lsb(input_path):
    """
    Odczytuje wiadomość ukrytą metodą LSB.
    """
    image = Image.open(input_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    pixels = image.load()

    width, height = image.size
    bits = []
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits.extend([format(r, '08b')[-1], format(g, '08b')[-1], format(b, '08b')[-1]])

    # Konwertuj bity na znaki
    chars = [chr(int(''.join(bits[i:i+8]), 2))
             for i in range(0, len(bits), 8)]
    message = ''.join(chars)
    delimiter = '====='
    if delimiter in message:
        return message.split(delimiter)[0]
    else:
        raise ValueError('Nie znaleziono znacznika końca wiadomości.')


def main():
    parser = argparse.ArgumentParser(description='LSB Steganography')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Encode
    enc = subparsers.add_parser('encode', help='Ukryj wiadomość w obrazie')
    enc.add_argument('input', help='Plik wejściowy (cover)')
    enc.add_argument('output', help='Plik wyjściowy (stego)')
    enc.add_argument('-m', '--message', required=True, help='Wiadomość do ukrycia')

    # Decode
    dec = subparsers.add_parser('decode', help='Odczytaj wiadomość z obrazu')
    dec.add_argument('input', help='Plik ze schowaną wiadomością')

    args = parser.parse_args()
    if args.command == 'encode':
        encode_lsb(args.input, args.output, args.message)
    else:
        text = decode_lsb(args.input)
        print('Odkodowana wiadomość:', text)


if __name__ == '__main__':
    main()

