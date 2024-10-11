import os
import math

def analyze_unicode_file(filename):
    """Анализирует текстовый файл с кодировкой UTF-8,
    считая символами Unicode.
    """

    # Инициализация словаря для хранения частот символов (Unicode)
    char_counts = {}

    # Чтение файла и подсчет частот символов
    total_chars = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('\n', '\r\n')
            for char in line:
                char_counts[char] = char_counts.get(char, 0) + 1
                total_chars += 1

    # Вычисление вероятностей, количества информации и оценок размера
    results = {
        'filename': filename,
        'total_chars': total_chars,
        'char_data': [],
        'I_total': 0.0
    }

    for char, count in char_counts.items():
        probability = count / total_chars
        if probability > 0:
            information = -math.log2(probability)
        else:
            information = 0
        results['char_data'].append({
            'char': char,
            'ord': ord(char),
            'count': count,
            'probability': probability,
            'information': information
        })
        results['I_total'] += information * count

    # Оценки размера сжатых данных
    results['I_total_bytes'] = results['I_total'] / 8
    results['E'] = math.floor(results['I_total_bytes'])

    # Оценка размера архива (учитываем размер словаря)
    alphabet_size = len(char_counts)
    results['G32'] = results['E'] + 8 + alphabet_size * (4 + 8)  # 64 бит (8 байт) длина алфавита, UTF-32 + частота
    results['G_utf8'] = results['E'] + 8
    for char, count in char_counts.items():
        char_len = len(char.encode('utf-8'))
        results['G_utf8'] += char_len + 8

    return results


def print_results(results):
    """Выводит результаты анализа файла в формате Unicode."""

    print(f"Анализ файла: {results['filename']}")
    print(f"Длина текста (символы Unicode): {results['total_chars']}")
    print(f"Суммарное количество информации I(Q) (бит): {results['I_total']:.2f}")
    print(f"I(Q) (доля от размера файла): {results['I_total'] / (results['total_chars'] * 8):.2e}")
    print(f"I(Q) (байт): {results['I_total_bytes']:.2f}")
    print(f"Оценка длины сжатого текста E (байт): {results['E']}")
    print(f"Оценка длины архива G32 (байт): {results['G32']}")
    print(f"Оценка длины архива G_utf8 (байт): {results['G_utf8']}\n")

    # Вывод таблицы характеристик символов, отсортированной по символу
    # print("Таблица характеристик символов (сортировка по символу):")
    # print("----------------------------------------------------------------")
    # print("| Символ | Код (dec) | Частота | Вероятность | I(символ) (бит) |")
    # print("----------------------------------------------------------------")
    # for item in sorted(results['char_data'], key=lambda x: x['ord']):
    #     print(f"| {item['char']:>7} | {item['ord']:>9} | {item['count']:>7} | {item['probability']:12.4f} | {item['information']:14.2f} |")
    # print("----------------------------------------------------------------\n")

    # # Вывод таблицы характеристик символов, отсортированной по частоте
    # print("Таблица характеристик символов (сортировка по частоте):")
    # print("----------------------------------------------------------------")
    # print("| Символ | Код (dec) | Частота | Вероятность | I(символ) (бит) |")
    # print("----------------------------------------------------------------")
    # for item in sorted(results['char_data'], key=lambda x: x['count'], reverse=True):
    #     print(f"| {item['char']:>7} | {item['ord']:>9} | {item['count']:>7} | {item['probability']:12.4f} | {item['information']:14.2f} |")
    # print("----------------------------------------------------------------")


# Пример использования:
filename = 'test.txt'
results = analyze_unicode_file(filename)
print_results(results)