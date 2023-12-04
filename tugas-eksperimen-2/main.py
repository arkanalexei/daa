import time
import tracemalloc
from dp import unboundedKnapsack
from bnb import KnapsackOptimizer, Item
from tabulate import tabulate

def read_data(filename):
    items = []
    with open(filename, 'r') as file:
        next(file)  # Skip header
        for line in file:
            weight, value = map(int, line.strip().split(','))
            items.append(Item(value, weight))
    return items

def run_experiment(method, items, W):
    tracemalloc.start()
    start_time = time.perf_counter()

    result = method(items, W)

    end_time = time.perf_counter()
    memory_used = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    time_taken = (end_time - start_time) * 1000
    memory_used = memory_used[1] - memory_used[0]
    return result, time_taken, memory_used

def dp_method(items, W):
    weights, values = zip(*[(item.wt, item.val) for item in items])
    return unboundedKnapsack(W, weights, values, len(values))

def bnb_method(items, W):
    optimizer = KnapsackOptimizer(W, items)
    optimizer.solve()
    return optimizer.get_optimized_val()

def print_results(results):
    headers = ["Method", "Dataset", "Result", "Time (ms)", "Memory (B)"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

datasets = {
    "kecil": 1000,
    "sedang": 10000,
    "besar": 100000
}

results = []
base_dir = "dataset/"

for name, W in datasets.items():
    filename = f"{base_dir}dataset_{name}.txt"
    items = read_data(filename)

    dp_result, dp_time, dp_memory = run_experiment(dp_method, items, W)
    results.append(["DP", name, dp_result, dp_time, dp_memory])

    bnb_result, bnb_time, bnb_memory = run_experiment(bnb_method, items, W)
    results.append(["BnB", name, bnb_result, bnb_time, bnb_memory])

print_results(results)
