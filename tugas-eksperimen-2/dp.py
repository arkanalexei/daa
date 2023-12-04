'''
Code for the unbounded knapsack problem using dynamic programming approach
is taken from https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/

The code is then refactored to use an iterative approach instead of recursive due to
Python's recursion limit.
'''

def unboundedKnapsack(W, wt, val, n): 
    dp = [0 for _ in range(W + 1)]

    for i in range(1, W + 1):
        for j in range(n):
            if wt[j] <= i:
                dp[i] = max(dp[i], dp[i - wt[j]] + val[j])

    return dp[W]


if __name__ == '__main__':
    W = 100
    val = [10, 30, 20]
    wt = [5, 10, 15]
    n = len(val)
    print(unboundedKnapsack(W, wt, val, n))
