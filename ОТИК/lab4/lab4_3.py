import sys
import heapq
from collections import Counter
import math

# Константы формата
SIGNATURE = b"52SPB!"
ALGO_NONE = 0
ALGO_RLE = 1
ALGORITHM_CODE = 1

def decode_0(input_file_name, output_file_name):
    # декодирует
    with open(input_file_name, 'rb') as input:
        signature = input.read(6)
        version = int.from_bytes(input.read(2), byteorder="big")
        
        data_len = int.from_bytes(input.read(8), byteorder="big")
        data = input.read(data_len)

    with open(output_file_name, "wb") as output:
        output.write(data)

def decode_10(input_filename, output_filename):
    def rle_decode(data: bytes) -> bytes:
        """Реализует алгоритм декодирования RLE."""
        decoded = bytearray()
        i = 0
        while i < len(data):
            count = data[i]
            byte = data[i+1]
            decoded.extend([byte] * count)
            i += 2
        return bytes(decoded)

    """Декодирует архив input_filename в файл output_filename."""
    with open(input_filename, "rb") as input_file:
        # Чтение заголовка
        signature = input_file.read(6)
        version = input_file.read(2)
        compression_algo_context = int.from_bytes(input_file.read(1), byteorder="big")
        compression_algo = int.from_bytes(input_file.read(1), byteorder="big")
        protection_algo = int.from_bytes(input_file.read(1), byteorder="big")
        original_size = int.from_bytes(input_file.read(8), byteorder="big")
        service_data_len = int.from_bytes(input_file.read(2), byteorder="big")

        # Чтение служебных данных и сжатых данных
        service_data = input_file.read(service_data_len)
        compressed_data = input_file.read()

        # Применение алгоритмов (пока заглушки)
        if compression_algo == ALGO_RLE:
            data = rle_decode(compressed_data)
        else:
            data = compressed_data

    with open(output_filename, "wb") as output_file:
        output_file.write(data)

def decode_11(input_file, output_file):
    def build_huffman_tree(freq_table):
        heap = [[weight, [char, ""]] for char, weight in freq_table.items()] # смимвол, частота -> узел с пустым кодом
        heapq.heapify(heap) # list -> min-heap
        while len(heap) > 1:
            lo = heapq.heappop(heap) # 2 узла с наименьшей частотой
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p)) # key = (len, alphabet)

    with open(input_file, 'rb') as f:
        signature = f.read(6)
        
        version = f.read(2)
        
        algorithm_code = int.from_bytes(f.read(1), 'little')
        if algorithm_code != ALGORITHM_CODE:
            raise ValueError("Неподдерживаемый код алгоритма")
        
        num_chars = int.from_bytes(f.read(1), 'little')
        freq_table = {}
        for _ in range(num_chars):
            char = int.from_bytes(f.read(1), 'little')
            freq = int.from_bytes(f.read(4), 'little')
            freq_table[char] = freq
        
        last_byte_bits = int.from_bytes(f.read(1), 'little')
        
        huffman_tree = build_huffman_tree(freq_table)
        huffman_codes = {code: char for char, code in huffman_tree}
        
        bit_buffer = ""
        while True:
            byte = f.read(1)
            if not byte:
                break
            bit_buffer += bin(byte[0])[2:].zfill(8)
        
        bit_buffer = bit_buffer[:-8 + last_byte_bits]
        
        with open(output_file, 'wb') as out:
            code = ""
            for bit in bit_buffer:
                code += bit
                if code in huffman_codes:
                    out.write(bytes([huffman_codes[code]]))
                    code = ""

def main_decode(input_filename, output_filename):
    """Декодирует архив input_filename в файл output_filename."""
    with open(input_filename, "rb") as input_file:
        # Чтение заголовка
        signature = input_file.read(6)
        if signature != SIGNATURE:
            raise ValueError("Неверная сигнатура!")
        version = input_file.read(2)
        if version == b"\x00\x00":
            return decode_0(input_filename, output_filename)
        elif version == b"\x01\x00":
            return decode_10(input_filename, output_filename)
        elif version == b"\x01\x01":
            return decode_11(input_filename, output_filename)
        else:
            raise ValueError("Неверная версия!")


def main():
    arguments = sys.argv[1:]
    if len(arguments) != 2:
        print("Неверное кол-во аргументов")
        return
    input_file, output_file = arguments
    
    try:
        main_decode(input_file, output_file)
    except ValueError as exc:
        print(exc.args[1])

main()


