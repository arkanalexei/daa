'''
Code for the unbounded knapsack problem using branch and bound approach
is taken from https://www.tandfonline.com/doi/pdf/10.1057/palgrave.jors.2601698?casa_token=EW35GGben2sAAAAA%3AVZt6DkysIcc7im289FIjHbV6Q3nZr2vYAH_HtWInlRnwryJnWsXKK87_g478Gof5mB_MDiz29IDO1eA

The pseudocode inside the PDF is then refactored to Python.
PDF is "An improved branch and bound algorithm for a strongly correlated unbounded knapsack problem"
by Y-J Seong, Y-G G, M-K Kang & C-W Kang

PDF is also included in this repository as reference.
'''

class Item:
    def __init__(self, val, wt):
        self.val = val
        self.wt = wt

class KnapsackOptimizer:
    def __init__(self, W, items):
        self.W = W
        self.items = sorted(items, key=lambda item: item.val/item.wt, reverse=True)
        self.M = [[0 for _ in range(W + 1)] for _ in range(len(items))]
        self.optimized_configuration = [0 for _ in range(len(items))]
        self.optimized_val = 0

    def eliminate_dominated_items(self):
        non_dominated = []
        for i in range(len(self.items)):
            dominated = False
            for j in range(len(self.items)):
                if i != j and self.items[j].wt <= self.items[i].wt and self.items[j].val >= self.items[i].val:
                    dominated = True
                    break
            if not dominated:
                non_dominated.append(self.items[i])
        self.items = non_dominated

    def calculate_upper_bound(self, remaining_W, current_val, index):
        if index < len(self.items) - 1:
            next_item_val = self.items[index + 1].val
            next_item_wt = self.items[index + 1].wt
            return current_val + (remaining_W // next_item_wt) * next_item_val
        else:
            return current_val

    def branch_and_bound(self, index, current_val, remaining_W):
        if index == len(self.items):
            if current_val > self.optimized_val:
                self.optimized_val = current_val
            return

        max_qty = remaining_W // self.items[index].wt
        for qty in range(max_qty + 1):
            new_val = current_val + qty * self.items[index].val
            new_W = remaining_W - qty * self.items[index].wt
            upper_bound = self.calculate_upper_bound(new_W, new_val, index)

            if upper_bound > self.optimized_val:
                self.optimized_configuration[index] = qty
                self.branch_and_bound(index + 1, new_val, new_W)

    def solve(self):
        self.eliminate_dominated_items()
        self.branch_and_bound(0, 0, self.W)

    def get_optimized_configuration(self):
        return self.optimized_configuration

    def get_optimized_val(self):
        return self.optimized_val

if __name__ == '__main__':
    W = 100
    items = [Item(10, 5), Item(30, 10), Item(20, 15)]
    optimizer = KnapsackOptimizer(W, items)
    optimizer.solve()
    print("Best val:", optimizer.get_best_val())
    print("Best item configuration:", optimizer.get_best_configuration())
