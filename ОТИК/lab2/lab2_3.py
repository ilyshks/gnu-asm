import os
import math

def analyze_file(filename):
  """Анализирует файл и вычисляет характеристики источника символов.

  Args:
    filename: Путь к файлу для анализа.

  Returns:
    Словарь с результатами анализа, включая частоты символов,
    вероятности, количество информации и оценки размера сжатых данных.
  """

  # Инициализация словаря для хранения частот символов (байт)
  char_counts = {}
  for i in range(256):
    char_counts[i.to_bytes(1, 'big')] = 0

  # Чтение файла и подсчет частот символов
  total_chars = 0
  with open(filename, 'rb') as f:
    while True:
      byte = f.read(1)
      if not byte:
        break
      char_counts[byte] += 1
      total_chars += 1

  # Вычисление вероятностей, количества информации и оценок размера
  results = {
      'filename': filename,
      'total_chars': total_chars,
      'char_data': [],  # Список для хранения данных о каждом символе
      'I_total': 0.0  # Суммарное количество информации
  }

  for char, count in char_counts.items():
    probability = count / total_chars # вероятность каждого символа
    if probability > 0:
      information = -math.log2(probability) # количество информации
    else:
      information = 0
    results['char_data'].append({
        'char': char.hex(),
        'count': count,
        'probability': probability,
        'information': information
    })
    results['I_total'] += information * count # суммарное количество информации

  # Оценки размера сжатых данных
  results['I_total_bytes'] = results['I_total'] / 8
  results['E'] = math.floor(results['I_total_bytes'])
  results['G64'] = results['E'] + 256 * 8
  results['G8'] = results['E'] + 256

  results['char_counts'] = char_counts

  return results


directory = ['labs_files', 'labs_var2']
number_octets = 10

def main():
    folder_path = directory[1]  # Путь к папке с файлами

    total_results = {
        'total_files': 0,
        'total_chars': 0,
        'total_I': 0.0,
        'char_counts': {}  # Общий словарь для подсчета частот октетов
    }

    for i in range(256):
        total_results['char_counts'][i.to_bytes(1, 'big')] = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Анализируем только .txt файлы
            filepath = os.path.join(folder_path, filename)
            results = analyze_file(filepath)
            # print_results(results, "results.txt")  # Вывод в консоль и файл results.txt

            total_results['total_files'] += 1
            total_results['total_chars'] += results['total_chars']
            total_results['total_I'] += results['I_total']
            for char, count in results['char_counts'].items():
                total_results['char_counts'][char] += count

    # Вывод итогов
    print("-" * 30)
    print("Итого:")
    print(f"Обработано файлов: {total_results['total_files']}")
    print(f"Общее количество байт: {total_results['total_chars']}")
    print(f"Общая информация I(Q) (бит): {total_results['total_I']:.2f}\n")

    # Сортировка и вывод 4-х самых частых октетов
    sorted_char_counts = sorted(total_results['char_counts'].items(),
                               key=lambda item: item[1], reverse=True)
    print(f"{number_octets} самых частых октета:")
    for i in range(number_octets):
        char, count = sorted_char_counts[i]
        print(f"0x{char.hex()}: {count} раз")
    
    # --- Добавлен код для анализа непечатных символов ---
    print(f"\n{number_octets} самых частых непечатных октета (ASCII):")
    non_printable_counts = [(char, count) for char, count in sorted_char_counts 
                             if ord(char) < 32 or ord(char) > 126]
    for i in range(min(number_octets, len(non_printable_counts))):
        char, count = non_printable_counts[i]
        print(f"0x{char.hex()}: {count} раз")

main()


# 0x00 и 0x04 являются управляющими символами, используемыми для обозначения конца строки или передачи данных.

# 0x20 — это обычный пробел, который часто встречается в тексте.

# 0xD0 может быть частью символа в зависимости от кодировки, например, кириллической буквы "Д" или "Р".