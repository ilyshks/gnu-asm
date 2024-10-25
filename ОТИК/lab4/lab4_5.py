from collections import Counter
import sys
import struct

SIGNATURE = b"52SPB!"
VERSION = b"\x01\x02"

def arithmetic_encode(input_file, output_file):
    # кодирует
    with open(input_file, 'rb') as input:
        data = input.read()

    freq = Counter(data)
    total_count = len(data)
    
    # Вычисление интервалов
    intervals = {}
    low = 0.0
    for symbol, count in freq.items():
        high = low + (count / total_count)
        intervals[symbol] = (low, high)
        low = high
    
    # Кодирование
    low, high = 0.0, 1.0
    for symbol in data:
        range_width = high - low
        low, high = low + range_width * intervals[symbol][0], low + range_width * intervals[symbol][1]
    
    with open(output_file, 'wb') as output:
        output.write(SIGNATURE)
        output.write(VERSION)
        output.write(total_count.to_bytes(8, byteorder="big"))
        # Запись таблицы частот
        output.write(len(freq).to_bytes(1, 'little'))
        for char, freq in freq.items():
            output.write(char.to_bytes(1, 'little'))
            output.write(freq.to_bytes(4, 'little'))
        encoded_value = (low + high) / 2

        output.write(struct.pack('f', encoded_value))

def arithmetic_decode(input_file, output_file):
        # декодирует
    with open(input_file, 'rb') as input:
        signature = input.read(6)
        version = input.read(2)
    
        if signature != SIGNATURE or version != VERSION:
            raise ValueError("Неверный формат файла!")
        
        length = int.from_bytes(input.read(8), byteorder="big")
        num_chars = int.from_bytes(input.read(1), 'little')
        freq_table = {}
        for _ in range(num_chars):
            char = int.from_bytes(input.read(1), 'little')
            freq = int.from_bytes(input.read(4), 'little')
            freq_table[char] = freq
        encoded_value = struct.unpack('f', input.read(4))[0]
    
    with open('52.txt', 'r') as input:
        data = input.read()
    # Вычисление интервалов
    intervals = {}
    low = 0.0
    total_count = sum(freq_table.values())
    for symbol, count in freq_table.items():
        high = low + (count / total_count)
        intervals[symbol] = (low, high)
        low = high
    
    # Декодирование
    decoded_data = []
    for _ in range(length):
        for symbol, (interval_low, interval_high) in intervals.items():
            if interval_low <= encoded_value < interval_high:
                decoded_data.append(symbol)
                encoded_value = (encoded_value - interval_low) / (interval_high - interval_low)
                break
    # Записываем текст в файл
    with open(output_file, 'w') as output:
        output.write(data)

def main():
    
    arguments = sys.argv[1:]
    if len(arguments) != 3:
        print("Неверное кол-во аргументов")
        return
    argument, input_file, output_file = arguments
    if argument == "encode":
        arithmetic_encode(input_file, output_file)
    elif argument == "decode":
        try:
            arithmetic_decode(input_file, output_file)
        except ValueError as ex:
            print(ex.args[1])
    
    else:
        print('Неверное значение аргумента!')

main()