import heapq
from collections import Counter
import sys

# Сигнатура и версия формата
SIGNATURE = b"52SPB!"
VERSION_1 = b"\x01\x01"  # Версия 1.1

# Код алгоритма
ALGORITHM_CODE = 1


VERSION_0 = b"\x00\x00"

def encode(input_file_name, output_file_name):
    # кодирует
    with open(input_file_name, 'rb') as input:
        data = input.read()
    data_len = len(data)

    with open(output_file_name, 'wb') as output:
        output.write(SIGNATURE)
        output.write(VERSION_0)
        output.write(data_len.to_bytes(8, byteorder="big"))
        output.write(data)


def decode(input_file_name, output_file_name):
    # декодирует
    with open(input_file_name, 'rb') as input:
        signature = input.read(6)
        version = input.read(2)
        if signature != SIGNATURE or version != VERSION_0:
            raise ValueError("Неверный формат файла!")
        
        data_len = int.from_bytes(input.read(8), byteorder="big")
        data = input.read(data_len)

    with open(output_file_name, "wb") as output:
        output.write(data)



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
        f.write(VERSION_1)
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
        if version != VERSION_1:
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


def main_encode(input_file, output_file, flag):
    if flag == 1:
        compress(input_file, output_file)
    else:
        with open(input_file, 'rb') as f:
            data = f.read()
        length = len(data)
        freq_table = Counter(data)
        huffman_tree = build_huffman_tree(freq_table)
        huffman_codes = {char: code for char, code in huffman_tree}
        compressed_size = 0
        for char, frequency in freq_table.items():
            compressed_size += len(huffman_codes[char]) * frequency
        if compressed_size >= length:
            return encode(input_file, output_file)
        return compress(input_file, output_file)

def main_decode(input_file, output_file):
    with open(input_file, 'rb') as f:
        signature = f.read(6)
        if signature != SIGNATURE:
            raise ValueError("Неверная сигнатура файла")
        
        version = f.read(2)
        if version != VERSION_1 and version != VERSION_0:
            raise ValueError("Несовместимая версия файла")
        if version == VERSION_0:
            return decode(input_file, output_file)
        return decompress(input_file, output_file)


def main():
    arguments = sys.argv[1:]
    if len(arguments) != 4:
        print("Неверное кол-во аргументов (flag=1 для принудительного сжатия)")
        return
    argument, input_file, output_file, flag = arguments
    if argument == "encode":
        main_encode(input_file, output_file, flag)
    elif argument == "decode":
        try:
            main_decode(input_file, output_file)
        except ValueError as ex:
            print(ex.args[0])
    
    else:
        print('Неверное значение аргумента!')

main()



