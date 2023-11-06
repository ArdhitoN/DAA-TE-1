from clustered_binary_insertion_sort import clustered_binary_insertion_sort
from randomized_quicksort import randomized_quicksort

import random
import time
import tracemalloc
import os

import matplotlib.pyplot as plt
import gc


def generate_unique_random_dataset(size):
    dataset = list(range(1, size + 1))
    random.shuffle(dataset)
    return dataset

def generate_and_save_dataset(size, status, file_name, min_value=1, max_value=1000):
    if status == "random":
        dataset =  generate_unique_random_dataset(size)
    elif status == "sorted":
        dataset = list(range(min_value, min_value + size))
    elif status == "reversed":
        dataset = list(range(min_value + size - 1, min_value - 1, -1))
    
    with open(file_name, 'w') as file:
        file.write('\n'.join(map(str, dataset)))
    return dataset


def measure_time_and_memory(func, *args):
    gc.collect()  
    tracemalloc.start()  

    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()  
    tracemalloc.stop() 

    time_taken = (end_time - start_time) * 1000  # in milliseconds
    memory_taken = peak   # in bytes

    return time_taken, memory_taken, result

def analyze_sorting_algorithms(sizes, statuses, data_folder):
    
    results = {status: {'Clustered Binary Insertion Sort': {'time': {}, 'memory': {}},
                        'Randomized Quicksort': {'time': {}, 'memory': {}}}
               for status in statuses}
    
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    results_folder = os.path.join(os.path.dirname(data_folder), 'results')
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

        
    for size in sizes:
        for status in statuses:
            file_name = f'{data_folder}/dataset_{size}_{status}.txt'
            dataset = generate_and_save_dataset(size, status, file_name)
            print(f"Dataset size: {size}, Status: {status}")

            dataset_cbis = dataset.copy()
            time_cbis, mem_cbis, _ = measure_time_and_memory(clustered_binary_insertion_sort, dataset_cbis)
            print(f"Clustered Binary Insertion Sort - Time: {time_cbis} ms, Memory: {mem_cbis} bytes")
            with open(os.path.join(results_folder, f'sorted_cbis_{size}_{status}.txt'), 'w') as f:
                f.write('\n'.join(map(str, dataset_cbis)))
                
            results[status]['Clustered Binary Insertion Sort']['time'][size] = time_cbis
            results[status]['Clustered Binary Insertion Sort']['memory'][size] = mem_cbis

            dataset_rqs = dataset.copy()
            time_rqs, mem_rqs, _ = measure_time_and_memory(randomized_quicksort, dataset_rqs, 0, size -1)
            print(f"Randomized Quicksort - Time: {time_rqs} ms, Memory: {mem_rqs} bytes")
            with open(os.path.join(results_folder, f'sorted_rqs_{size}_{status}.txt'), 'w') as f:
                f.write('\n'.join(map(str, dataset_rqs)))
                
            results[status]['Randomized Quicksort']['time'][size] = time_rqs
            results[status]['Randomized Quicksort']['memory'][size] = mem_rqs
                
            print()

    plot_results(sizes, statuses, results)
    
    
def plot_results(sizes, statuses, results, file_name='sorting_performance_results.png'):
    # Membuat subplot
    fig, ax = plt.subplots(len(statuses), 2, figsize=(12, 4 * len(statuses)))

    for i, status in enumerate(statuses):
        # Time plot
        ax[i, 0].plot(sizes, [results[status]['Clustered Binary Insertion Sort']['time'][j] for j in sizes], 'o-', label='CBIS')
        ax[i, 0].plot(sizes, [results[status]['Randomized Quicksort']['time'][j] for j in sizes], 's-', label='RQS')
        ax[i, 0].set_title(f'Time Taken for {status.capitalize()} Data')
        ax[i, 0].set_xlabel('Dataset Size')
        ax[i, 0].set_ylabel('Time (ms)')
        ax[i, 0].legend()

        # Memory plot 
        cbis_memory = [results[status]['Clustered Binary Insertion Sort']['memory'][j] for j in sizes]
        rqs_memory = [results[status]['Randomized Quicksort']['memory'][j] for j in sizes]
        ax[i, 1].plot(sizes, cbis_memory, 'o-', label='CBIS')
        ax[i, 1].plot(sizes, rqs_memory, 's-', label='RQS')
        ax[i, 1].set_title(f'Peak Memory Usage for {status.capitalize()} Data')
        ax[i, 1].set_xlabel('Dataset Size')
        ax[i, 1].set_ylabel('Memory (bytes)')
        ax[i, 1].legend()
        
    plt.tight_layout()
    
    plt.savefig(file_name, dpi=300)
    plt.close(fig)  
    
if __name__ == "__main__":
    sizes = [200, 2000, 20000]
    statuses = ["random", "sorted", "reversed"]
    data_folder = 'datasets'
    
    analyze_sorting_algorithms(sizes, statuses, data_folder)
