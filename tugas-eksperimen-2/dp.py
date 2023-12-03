'''
Code for the unbounded knapsack problem using dynamic programming approach
is taken from https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/

The code is then refactored to use an iterative approach instead of recursive due to
Python's recursion limit.
'''

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


def unboundedKnapsack(W, wt, val, n): 
    dp = [0 for _ in range(W + 1)]

    for i in range(1, W + 1):
        for j in range(n):
            if wt[j] <= i:
                dp[i] = max(dp[i], dp[i - wt[j]] + val[j])

    return dp[W]

filename = "dataset/dataset_contoh.txt"
wt, val = read_data_from_file(filename)
W = 100
n = len(val)
print(unboundedKnapsack(W, wt, val, n))

filename = "dataset/dataset_kecil.txt"  
wt, val = read_data_from_file(filename)
W = 100
n = len(val)
print(unboundedKnapsack(W, wt, val, n))

filename = "dataset/dataset_sedang.txt"
wt, val = read_data_from_file(filename)
W = 1000
n = len(val)
print(unboundedKnapsack(W, wt, val, n))

filename = "dataset/dataset_besar.txt"
wt, val = read_data_from_file(filename)
W = 10000
n = len(val)
print(unboundedKnapsack(W, wt, val, n))