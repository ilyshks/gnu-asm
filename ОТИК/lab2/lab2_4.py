import sys
import math
from collections import defaultdict

def read_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

def read_file_symbols(filename):
    with open(filename, 'r') as file:
        return file.read()

def count_ajak(data):
    counts = defaultdict(int)
    for i in range(len(data) - 1):
        aj = data[i]
        ak = data[i + 1]
        counts[(aj, ak)] += 1
    return counts

def count_aj_star(data):
    counts = defaultdict(int)
    for i in range(len(data) - 1):
        aj = data[i]
        counts[aj] += 1
    return counts

def calculate_conditional_probabilities(ajak_counts, aj_star_counts):
    probabilities = defaultdict(dict)
    for (aj, ak), count in ajak_counts.items():
        probabilities[aj][ak] = count / aj_star_counts[aj]
    return probabilities

def calculate_information(data, probabilities):
    total_info = 0
    for i in range(len(data) - 1):
        aj = data[i]
        ak = data[i + 1]
        p_ak_given_aj = probabilities[aj][ak]
        total_info -= p_ak_given_aj * log2(p_ak_given_aj)
    return total_info

def log2(x):
    return math.log(x) / math.log(2)

def hex_format(byte):
    return f'{byte:02X}'

def hex_format_symbols(s):
    byte = ord(s)
    return f'{byte:02X}'

def main():
    filename = "test.txt"
    #data = read_file(filename)
    data = read_file_symbols(filename)
    
    ajak_counts = count_ajak(data)
    aj_star_counts = count_aj_star(data)
    
    probabilities = calculate_conditional_probabilities(ajak_counts, aj_star_counts)
    
    total_info = calculate_information(data, probabilities)
    
    print(f"Total information in bits: {total_info}")
    print(f"Total information in bytes: {total_info / 8}")

    hex_format = hex_format_symbols # убрать для номера 4


    print("ajak_counts:")
    for (i, ((aj, ak), count)) in enumerate(ajak_counts.items()):
        print(f"({hex_format(aj)}, {hex_format(ak)}): {count}")
        if i > 20:
            break
    
    print("\naj_star_counts:")
    for (i, (aj, count)) in enumerate(aj_star_counts.items()):
        print(f"{hex_format(aj)}: {count}")
        if i > 20:
            break
    

    print(*list(probabilities.items())[:5], sep='\n\n')

main()



# Пояснения:

# Подсчет пар: Вместо char_counts используем pair_counts для хранения частот пар байт. Добавлен prev_byte для отслеживания предыдущего байта.

# Условная вероятность: conditional_prob рассчитывается как отношение count(a_j a_k) / count(a_j *), где count(a_j *) - это частота char1 в парах.

# Информация: Рассчитывается I(a_k | a_j), то есть количество информации, необходимое для указания a_k, если известно, что предыдущим символом был a_j.

# Суммарная информация:

# Для первого символа используется безусловная вероятность 1/256.

# Для остальных символов - условная вероятность, рассчитанная на основе частот пар.

# Размер таблицы частот:

# Для декодирования нужно сохранить 256 * 256 = 65536 условных вероятностей (для каждой возможной пары байт).

# Если хранить каждую вероятность как 4-байтовое число с плавающей точкой, размер таблицы составит 65536 * 4 = 262144 байта (256 КБ).

# Выгодно ли такое сжатие?

# Сжатие с использованием модели Маркова первого порядка может быть выгоднее для файлов, где есть явные зависимости между соседними байтами.

# Однако, большой размер таблицы частот (256 КБ) может нивелировать выгоду от сжатия, особенно для небольших файлов.

# Необходимость хранения таблицы частот делает этот метод менее практичным для сжатия отдельных небольших файлов по сравнению с методами без учета контекста (Л2.№1) или с методами сжатия с использованием скользящего окна (LZ77, LZ78 и т.д.).