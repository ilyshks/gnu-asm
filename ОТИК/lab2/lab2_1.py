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

  return results

def print_results(results):
  """Выводит результаты анализа файла."""

  print(f"Анализ файла: {results['filename']}")
  print(f"Длина файла (байт): {results['total_chars']}")
  print(f"Длина файла (бит): {results['total_chars'] * 8}")
  print(f"Суммарное количество информации I(Q) (бит): {results['I_total']:.2f}")
  print(f"I(Q) (доля от размера файла): {results['I_total'] / (results['total_chars'] * 8):.2e}")
  print(f"I(Q) (байт): {results['I_total_bytes']:.2f}")
  print(f"Оценка длины сжатого текста E (байт): {results['E']}")
  print(f"Оценка длины архива G64 (байт): {results['G64']}")
  print(f"Оценка длины архива G8 (байт): {results['G8']}\n")

  # Вывод таблицы характеристик символов, отсортированной по символу
#   print("Таблица характеристик символов (сортировка по символу):")
#   print("-----------------------------------------------------")
#   print("| Символ | Частота | Вероятность | I(символ) (бит) |")
#   print("-----------------------------------------------------")
#   for item in sorted(results['char_data'], key=lambda x: x['char']):
#     print(f"| {item['char']:>7} | {item['count']:>7} | {item['probability']:12.4f} | {item['information']:14.2f} |")
#   print("-----------------------------------------------------\n")

#   # Вывод таблицы характеристик символов, отсортированной по частоте
#   print("Таблица характеристик символов (сортировка по частоте):")
#   print("-----------------------------------------------------")
#   print("| Символ | Частота | Вероятность | I(символ) (бит) |")
#   print("-----------------------------------------------------")
#   for item in sorted(results['char_data'], key=lambda x: x['count'], reverse=True):
#     print(f"| {item['char']:>7} | {item['count']:>7} | {item['probability']:12.4f} | {item['information']:14.2f} |")
#   print("-----------------------------------------------------")

# Пример использования:
filename = 'test.txt'  # Замените на имя вашего файла
results = analyze_file(filename)
print_results(results)

filename = 'test.bin'  # Замените на имя вашего файла
results = analyze_file(filename)
print_results(results)