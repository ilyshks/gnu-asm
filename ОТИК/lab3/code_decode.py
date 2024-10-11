import sys


SIGNATURE = b"52SPB!"
VERSION = 0

def encode(input_file_name, output_file_name):
    # кодирует
    with open(input_file_name, 'rb') as input:
        data = input.read()
    data_len = len(data)

    with open(output_file_name, 'wb') as output:
        output.write(SIGNATURE)
        output.write(VERSION.to_bytes(2, byteorder="big"))
        output.write(data_len.to_bytes(8, byteorder="big"))
        output.write(data)


def decode(input_file_name, output_file_name):
    # декодирует
    with open(input_file_name, 'rb') as input:
        signature = input.read(6)
        version = int.from_bytes(input.read(2), byteorder="big")
    
        if signature != SIGNATURE or version != VERSION:
            raise ValueError("Неверный формат файла!")
        
        data_len = int.from_bytes(input.read(8), byteorder="big")
        data = input.read(data_len)

    with open(output_file_name, "wb") as output:
        output.write(data)
    


def main():
    arguments = sys.argv[1:]
    if len(arguments) != 3:
        print("Неверное кол-во аргументов")
        return
    argument, input_file, output_file = arguments
    if argument == "encode":
        encode(input_file, output_file)
    elif argument == "decode":
        try:
            decode(input_file, output_file)
        except ValueError as ex:
            print(ex.args[0])
    
    else:
        print('Неверное значение аргумента!')

main()
