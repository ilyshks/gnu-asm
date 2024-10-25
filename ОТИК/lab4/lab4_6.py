import os
from collections import defaultdict

SIGNATURE = b"52SPB!"
VERSION = b"\x01\x03"  # Версия 1.3

class Shannon:
    def __init__(self):
        self.codes = {}

    def make_frequency_dict(self, text):
        frequency = defaultdict(int)
        for symbol in text:
            frequency[symbol] += 1
        return frequency

    def shannon_fano_codes(self, frequency):
        def assign_codes(symbols, prefix=""):
            if len(symbols) == 1:
                self.codes[symbols[0][0]] = prefix
                return
            total_freq = sum(freq for _, freq in symbols)
            half_freq = 0
            for i, (symbol, freq) in enumerate(symbols):
                half_freq += freq
                if half_freq >= total_freq / 2:
                    assign_codes(symbols[:i+1], prefix + "0")
                    assign_codes(symbols[i+1:], prefix + "1")
                    return

        sorted_symbols = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        assign_codes(sorted_symbols)

    def get_encoded_text(self, text):
        encoded_text = ''
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += '0' * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + ".spb"

        with open(input_path, 'r') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)
            self.shannon_fano_codes(frequency)

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(SIGNATURE)
            output.write(VERSION)
            output.write(bytes(b))

        print("Compressed")
        return output_path

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.codes.values():
                character = [k for k, v in self.codes.items() if v == current_code][0]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed_shennon" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""
            signature = file.read(6)
            version = file.read(2)
            if signature != SIGNATURE and version != VERSION:
                raise ValueError("Неверный формат файла!")
            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)
            
            output.write(decompressed_text)

        print("Decompressed")
        return output_path

# Пример использования
shannon = Shannon()
compressed_file_path = shannon.compress('52.txt')
try:
    decompressed_file_path = shannon.decompress(compressed_file_path)
except ValueError as exc:
    print(exc.args[1])