import heapq
from collections import Counter
import math

# Сигнатура и версия формата
SIGNATURE = b"52SPB!"
VERSION = b"\x01\x01"  # Версия 1.1

# Код алгоритма
ALGORITHM_CODE = 1


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

def compress(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    length = len(data)
    freq_table = Counter(data)
    huffman_tree = build_huffman_tree(freq_table)
    huffman_codes = {char: code for char, code in huffman_tree}
    
    # Запись сигнатуры, версии и кода алгоритма
    with open(output_file, 'wb') as f:
        f.write(SIGNATURE)
        f.write(VERSION)
        f.write(ALGORITHM_CODE.to_bytes(1, 'little'))
        
        # Запись таблицы частот
        f.write(len(freq_table).to_bytes(1, 'little'))
        for char, freq in freq_table.items():
            f.write(char.to_bytes(1, 'little'))
            f.write(freq.to_bytes(4, 'little'))
        
        # Запись сжатых данных
        bit_buffer = ""
        for char in data:
            bit_buffer += huffman_codes[char]
        
        # Дополнение до целого числа байт
        padding = 8 - len(bit_buffer) % 8
        bit_buffer += '0' * padding
        
        # Запись количества битов в последнем байте
        f.write((8 - padding).to_bytes(1, 'little'))
        
        # Запись сжатых данных
        for i in range(0, len(bit_buffer), 8):
            byte = bit_buffer[i:i+8]
            f.write(int(byte, 2).to_bytes(1, 'little'))
    return length, freq_table

def decompress(input_file, output_file):
    with open(input_file, 'rb') as f:
        signature = f.read(6)
        if signature != SIGNATURE:
            raise ValueError("Неверная сигнатура файла")
        
        version = f.read(2)
        if version != VERSION:
            raise ValueError("Несовместимая версия файла")
        
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
    with open(input_file, 'rb') as f:
        return len(f.read())

# Пример использования
length, freq_table = compress("52.txt", "52_compressed.spb")
compressed_length = 0
try:
    compressed_length = decompress("52_compressed.spb", "52_decompressed.txt")
except ValueError as exc:
    print(exc.args[1])

I = 0
for char in freq_table:
    I += -math.log2(freq_table[char] / length)

E = int(I / 8)
G = E + len(freq_table) * 5 + 1
print(f'Длина сжатого файла = {compressed_length}')
print(f"I = {I}")
print(f'Длина архива = {G}')

