import argparse

# Константы формата
SIGNATURE = b"52SPB!"
VERSION = b"\x01\x00"  # Версия 1.0

# Коды алгоритмов (пока только заглушки)
ALGO_NONE = 0
ALGO_RLE = 1

def encode(input_filename, output_filename, compression_algo=ALGO_NONE, protection_algo=ALGO_NONE):
    """Кодирует файл input_filename в архив output_filename."""

    with open(input_filename, "rb") as input_file:
        data = input_file.read()

    # Применение алгоритмов (пока заглушки)
    if compression_algo == ALGO_RLE:
        compressed_data = rle_encode(data)
        service_data = b""  # RLE не требует служебных данных
    else:
        compressed_data = data
        service_data = b""

    data_len = len(compressed_data)
    service_data_len = len(service_data)

    with open(output_filename, "wb") as output_file:
        # Запись заголовка
        output_file.write(SIGNATURE)
        output_file.write(VERSION)
        output_file.write(bytes([ALGO_NONE]))  # Код алгоритма сжатия с учетом контекста
        output_file.write(bytes([compression_algo])) # Код алгоритма сжатия без учета контекста
        output_file.write(bytes([protection_algo])) # Код алгоритма защиты от помех
        output_file.write(data_len.to_bytes(8, byteorder="big")) # Исходная длина файла
        output_file.write(service_data_len.to_bytes(2, byteorder="big")) # Размер блока служебных данных

        # Запись служебных данных и сжатых данных
        output_file.write(service_data)
        output_file.write(compressed_data)


def decode(input_filename, output_filename):
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

        if signature != SIGNATURE:
            raise ValueError("Неверная сигнатура файла!")

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


def rle_encode(data: bytes) -> bytes:
    """Реализует алгоритм сжатия RLE."""
    if len(data) == 0:
        return b""
    encoded = bytearray()
    count = 1
    prev_byte = data[0]
    for i in range(1, len(data)):
        if data[i] == prev_byte and count < 255:
            count += 1
        else:
            encoded.append(count)
            encoded.append(prev_byte)
            prev_byte = data[i]
            count = 1
    encoded.append(count)
    encoded.append(prev_byte)
    return bytes(encoded)


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


parser = argparse.ArgumentParser(description="Архиватор файлов.")
parser.add_argument("mode", choices=["encode", "decode"], help="Режим работы: encode или decode.")
parser.add_argument("input_file", help="Путь к входному файлу.")
parser.add_argument("output_file", help="Путь к выходному файлу.")
parser.add_argument("-c", "--compression", choices=[ALGO_NONE, ALGO_RLE], type=int, default=ALGO_NONE, 
                    help="Алгоритм сжатия: 0 - без сжатия (по умолчанию), 1 - RLE")
parser.add_argument("-p", "--protection", choices=[ALGO_NONE], type=int, default=ALGO_NONE,
                    help="Алгоритм защиты: 0 - без защиты (по умолчанию)")

args = parser.parse_args()
if args.mode == "encode":
    encode(args.input_file, args.output_file, args.compression, args.protection)
elif args.mode == "decode":
    try:
        decode(args.input_file, args.output_file)
    except ValueError as ex:
        print(ex.args[0])

