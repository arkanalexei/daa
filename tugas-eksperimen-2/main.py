import time
import tracemalloc
from dp import unboundedKnapsack
from bnb import KnapsackOptimizer, Item
from tabulate import tabulate

def read_data_from_file(filename):
    items = []
    with open(filename, 'r') as file:
        next(file)
        for line in file:
            weight, value = line.strip().split(',')
            items.append(Item(int(value), int(weight)))
    return items

def run_experiment(method_function, items, capacity, runs=10):
    total_time = 0
    total_memory = 0
    for _ in range(runs):
        tracemalloc.start()
        start_time = time.perf_counter()

        result = method_function(items, capacity)

        end_time = time.perf_counter()
        memory_used = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        total_time += end_time - start_time
        total_memory += memory_used[1] - memory_used[0]

    avg_time = total_time / runs * 1000
    avg_memory = total_memory / runs
    return result, avg_time, avg_memory

def print_results(results):
    headers = ["Method", "Result", "Avg Time (ms)", "Avg Memory (B)"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

results = []
base_dir = "dataset/"
datasets = [f"{base_dir}dataset_kecil.txt", f"{base_dir}dataset_sedang.txt", f"{base_dir}dataset_besar.txt"]

for filename in datasets:
    items = read_data_from_file(filename)
    W = 100

    # Run DP
    wt, val = zip(*[(item.wt, item.val) for item in items])
    result, dp_time, dp_memory = run_experiment(lambda i, c: unboundedKnapsack(c, list(wt), list(val), len(val)), items, W)
    results.append(["DP", result, f"{dp_time:.6f}", f"{dp_memory}"])

    # Run BnB
    optimizer = KnapsackOptimizer(W, items)
    result, bnb_time, bnb_memory = run_experiment(lambda i, c: optimizer.solve() or optimizer.get_optimized_val(), items, W)
    results.append(["BnB", result, f"{bnb_time:.6f}", f"{bnb_memory}"])

print_results(results)
