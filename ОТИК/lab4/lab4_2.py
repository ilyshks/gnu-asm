import heapq
from collections import Counter
import os
import matplotlib.pyplot as plt


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

def build_huffman_codes(huffman_tree):
    return {char: code for char, code in huffman_tree}

def normalize_frequencies(frequencies, bits):
    max_freq = max(frequencies.values())
    return {char: int(freq * (2**bits - 1) / max_freq) for char, freq in frequencies.items()}

def count_frequencies(file_path):

    with open(file_path, 'rb') as file:
        data = file.read()

    return Counter(data)

def calculate_compressed_length(frequencies, code_map):
    total_length = 0
    for freq, code in zip(frequencies, code_map.values()):
        total_length += freq * len(code)
    return (total_length + 7) // 8  # Convert bits to bytes

def calculate_total_length(compressed_length, bits):
    return compressed_length + 32 * bits


def find_optimal_bit_size(file_path):
    frequencies = count_frequencies(file_path)
    min_gb = float('inf')
    optimal_bits = 64
    
    for bits in range(1, 65):
        normalized_freqs = normalize_frequencies(frequencies, bits)
        huffman_tree = build_huffman_tree(normalized_freqs)
        code_map = build_huffman_codes(huffman_tree)
        compressed_length = calculate_compressed_length(normalized_freqs, code_map)
        total_length = calculate_total_length(compressed_length, bits)
        
        if total_length < min_gb:
            min_gb = total_length
            optimal_bits = bits
    
    return optimal_bits

def compare_files(file_paths):
    results = []
    for file_path in file_paths:
        frequencies = count_frequencies(file_path)
        file_results = {}
        
        for bits in range(1, 65):
            normalized_freqs = normalize_frequencies(frequencies, bits)
            huffman_tree = build_huffman_tree(normalized_freqs)
            code_map = build_huffman_codes(huffman_tree)
            compressed_length = calculate_compressed_length(normalized_freqs, code_map)
            total_length = calculate_total_length(compressed_length, bits)
            file_results[f'E{bits}'] = compressed_length
            file_results[f'G{bits}'] = total_length
        
        file_results['B*'] = find_optimal_bit_size(file_path)
        results.append(file_results)
    
    return results


directory = 'files'
file_paths = []
for filename in os.listdir(directory):
    file_paths.append(os.path.join(directory, filename))
results = compare_files(file_paths)

for i, result in enumerate(results):
    print(file_paths[i], result['B*'])

def plot_results(results):
    E_values = {filename: [] for filename in file_paths}
    G_values = {filename: [] for filename in file_paths}
    
    for i, result in enumerate(results):
        for bits in range(1, 65):
            E_values[file_paths[i]].append(result[f'E{bits}'] / result['E64'])
            G_values[file_paths[i]].append(result[f'G{bits}'] / result['G64'])
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    for filename in file_paths:
        plt.plot(range(1, 65), E_values[filename], label=f'Eb/E64 {filename}')
    plt.title('Зависимость E от B')
    plt.xlabel('Файл')
    plt.ylabel('Длина сжатых данных (байты)')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    for filename in file_paths:
        plt.plot(range(1, 65), G_values[filename], label=f'Gb/G64 {filename}')
    plt.title('Зависимость G от B')
    plt.xlabel('Файл')
    plt.ylabel('Общая длина данных для распаковки (байты)')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

plot_results(results)