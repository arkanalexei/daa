import time
import tracemalloc
from dp import unboundedKnapsack
from bnb import KnapsackOptimizer
from tabulate import tabulate


def read_data_from_file(filename):
    weights = []
    values = []
    with open(filename, 'r') as file:
        next(file)
        for line in file:
            weight, value = line.strip().split(',')
            weights.append(int(weight))
            values.append(int(value))
    return weights, values

def run_experiment(method_function, weights, values, capacity, runs=10):
    total_time = 0
    total_memory = 0
    for _ in range(runs):
        tracemalloc.start()
        start_time = time.perf_counter()

        result = method_function(weights, values, capacity)

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
    wt, val = read_data_from_file(filename)
    W = 100

    # Run DP
    result, dp_time, dp_memory = run_experiment(lambda w, v, c: unboundedKnapsack(c, w, v, len(v)), wt, val, W)
    results.append(["DP", result, f"{dp_time:.6f}", f"{dp_memory}"])

    # Run BnB
    result, bnb_time, bnb_memory = run_experiment(lambda w, v, c: KnapsackOptimizer(c, w, v).execute_branch_and_bound()[1], wt, val, W)
    results.append(["BnB", result, f"{bnb_time:.6f}", f"{bnb_memory}"])

print_results(results)