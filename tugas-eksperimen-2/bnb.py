import math

class BranchAndBound:
    def __init__(self, W, wt, val, n):
        self.W = W
        self.n = n
        self.items = [{'value': val[i], 'weight': wt[i]} for i in range(n)]
        print("lol", self.items)
        self.M = None
        self.best_solution = None
        self.best_value = None

    def eliminate_dominated_items(self):
        self.items.sort(key=lambda x: x['value'] / x['weight'], reverse=True)
        filtered_items = []

        for item in self.items:
            if not any(dominating_item['weight'] <= item['weight'] and dominating_item['value'] >= item['value'] for dominating_item in filtered_items):
                filtered_items.append(item)

        self.items = filtered_items
        self.n = len(filtered_items)
    
    def calculate_upper_bound(self, W_prime, V_N, i):
        if i + 2 < self.n:
            item1 = self.items[i]
            item2 = self.items[i + 1]
            item3 = self.items[i + 2]

            z_prime = V_N + (W_prime // item2['weight']) * item2['value']
            W_double_prime = W_prime - (W_prime // item2['weight']) * item2['weight']
            U_prime = z_prime + (W_double_prime * item3['value'] // item3['weight'])

            W_double_prime_adjusted = W_double_prime + math.ceil((1 / item1['weight']) * (item2['weight'] - W_double_prime)) * item1['weight']
            U_double_prime = z_prime + math.floor((W_double_prime_adjusted * item2['value'] / item2['weight']) - math.ceil((1 / item1['weight']) * (item2['weight'] - W_double_prime)) * item1['value'])

            U = max(U_prime, U_double_prime)
        else:
            U = V_N
        return U

    def step1_initialize(self):
        self.eliminate_dominated_items()
        self.M = [[0 for _ in range(self.W + 1)] for _ in range(self.n)]
        self.best_solution = [0 for _ in range(self.n)]
        self.best_value = 0

        x = [0 for _ in range(self.n)]
        i = 0
        x[0] = self.W // self.items[0]['weight']
        V_N = self.items[0]['value'] * x[0]
        W_prime = self.W - self.items[0]['weight'] * x[0]
        U = self.calculate_upper_bound(W_prime, V_N, i)
        self.best_value = V_N
        self.best_solution = x.copy()

        m = [float('inf') for _ in range(self.n)]
        for idx in range(1, self.n):
            for j in range(idx):
                if self.items[j]['weight'] < m[idx]:
                    m[idx] = self.items[j]['weight']
        return x, i, V_N, W_prime, U, m

    def step2_develop(self, x, i, V_N, W_prime, U, m):
        while True:
            if W_prime < m[i]:
                if self.best_value < V_N:
                    self.best_value = V_N
                    self.best_solution = x.copy()
                    if self.best_value == U:
                        return x, i, V_N, W_prime, "Finish"
                return x, i, V_N, W_prime, "Backtrack"
            else:
                min_j = min((j for j in range(i + 1, self.n) if self.items[j]['weight'] <= W_prime), default=None)
                if min_j is None or (V_N + self.calculate_upper_bound(W_prime, V_N, min_j) <= self.best_value):
                    return x, i, V_N, W_prime, "Backtrack"
                if self.M[i][W_prime] >= V_N:
                    return x, i, V_N, W_prime, "Backtrack"
                x[min_j] = W_prime // self.items[min_j]['weight']
                V_N += self.items[min_j]['value'] * x[min_j]
                W_prime -= self.items[min_j]['weight'] * x[min_j]
                self.M[i][W_prime] = V_N
                i = min_j
                return x, i, V_N, W_prime, "Develop"
    
    def step3_backtrack(self, x, i, V_N, W_prime, m):
        while True:
            max_j = max((j for j in range(i + 1) if x[j] > 0), default=None)
            if max_j is None:
                return x, i, V_N, W_prime, "Finish"
            i = max_j
            x[i] -= 1
            V_N -= self.items[i]['value']
            W_prime += self.items[i]['weight']
            if W_prime < m[i]:
                continue
            if V_N + math.floor(W_prime * self.items[i + 1]['value'] / self.items[i + 1]['weight']) <= self.best_value:
                V_N -= self.items[i]['value'] * x[i]
                W_prime += self.items[i]['weight'] * x[i]
                x[i] = 0
                continue
            return x, i, V_N, W_prime, "Develop"

    def branch_and_bound(self):
        x, i, V_N, W_prime, U, m = self.step1_initialize()
        next_step = "Develop"
        while next_step != "Finish":
            if next_step == "Develop":
                x, i, V_N, W_prime, next_step = self.step2_develop(x, i, V_N, W_prime, U, m)
            elif next_step == "Backtrack":
                x, i, V_N, W_prime, next_step = self.step3_backtrack(x, i, V_N, W_prime, m)
        return self.best_solution, self.best_value

    def solve(self):
        return self.branch_and_bound()

if __name__ == '__main__':
    W = 100
    val = [10, 30, 20]
    wt = [5, 10, 15]

    bnb = BranchAndBound(W, wt, val, len(wt))
    solution, value = bnb.solve()

    print(f"W (knapsack capacity): {W}")
    print(f"Items <value, weight>: {list(zip(val, wt))}")
    print(f"Best value: {value}")
    print(f"Best item configuration: {solution}")                   